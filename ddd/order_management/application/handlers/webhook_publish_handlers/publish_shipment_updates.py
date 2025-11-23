from __future__ import annotations
import json
import logging
from ddd.order_management.application import (
    ports, 
    dtos,
    commands
)
from ddd.order_management.domain import exceptions


def handle_publish_shipment_updates(
    command: commands.PublishShipmentUpdatesCommand, 
    uow: ports.UnitOfWorkAbstract, # uow is unused, consider removing or using it
    exception_handler: ports.ExceptionHandlerAbstract,
    user_action_service: ports.UserActionServiceAbstract, # unused, consider removing
    webhook_receiver_service: ports.WebhookReceiverServiceAbstract,
    shipment_repo: ports.ShipmentRepositoryAbstract, # Use abstract type hint
    shipping_webhook_resolver: ports.ShippingWebhookResolverAbstract,
    event_publisher: ports.EventPublisherAbstract
) -> dtos.ResponseDTO:
    """
    Processes an incoming EasyPost webhook request within a DDD context.
    """
    try:
        # Use command.raw_body directly, which should already be bytes/str
        # Decode robustly; request is assumed to be an infrastructure detail passed in via command
        try:
            payload_data = json.loads(command.raw_body)
        except json.JSONDecodeError:
            # Re-raise with context or return a specific handler error
            raise exceptions.InvalidOrderOperation("Invalid JSON payload received.")
        
        # EasyPost webhooks use "tracker.created" or similar event structures
        # We need to adapt the key lookup based on actual webhook structure.
        # Assuming the tracking code is nested, adjust lookup paths as necessary:
        tracking_reference = payload_data.get("result", {}).get("tracking_code") or \
                             payload_data.get("tracking_code") 

        if not tracking_reference:
            raise exceptions.InvalidOrderOperation("Tracking reference missing from payload.")

        # --- Core Logic Streamlined ---

        # Assuming shipment_repo can find a tenant ID associated with the tracking ref
        # This part requires specific implementation details based on your data model
        tenant_id = shipment_repo.get_tenant_id_by_tracking_ref(tracking_reference)
        
        # Validation uses the raw body provided in the command DTO
        validated_payload = webhook_receiver_service.validate(
            tenant_id, 
            command.headers,
            command.raw_body,
            command.request_path
        )

        normalized_event_data = shipping_webhook_resolver.resolve(
            tenant_id=tenant_id,
            payload=validated_payload # Use the validated payload
        )

        event = dtos.ShippingWebhookIntegrationEvent(
            **normalized_event_data
        )

        event_publisher.publish(event)
        
        # The UOW is the standard place to commit work in DDD apps
        # If operations change state, commit here
        # uow.commit() 

        return dtos.ResponseDTO(
            success=True,
            message="Shipment updates have been published to queue."
        )

    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

