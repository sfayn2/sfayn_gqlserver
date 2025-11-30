from __future__ import annotations
import json
import logging
from ddd.order_management.application import (
    ports, 
    dtos,
    commands,
    mappers
)
from ddd.order_management.domain import exceptions


def handle_publish_shipment_tracker_tenant(
    command: commands.PublishShipmentTrackerTenantCommand, 
    uow: ports.UnitOfWorkAbstract,
    user_action_service: ports.UserActionServiceAbstract,
    exception_handler: ports.ExceptionHandlerAbstract,
    webhook_receiver_service: ports.WebhookReceiverServiceAbstract,
    shipment_lookup_service: ports.ShipmentLookupServiceAbstract,
    shipping_webhook_resolver: ports.ShippingWebhookResolverAbstract,
    event_publisher: ports.EventPublisherAbstract
) -> dtos.ResponseDTO:
    """
    Processes an incoming Shipping provider webhook request within a DDD context.
    """
    try:

        validated_payload = webhook_receiver_service.validate(
            tenant_id=command.tenant_id,
            headers=command.headers,
            raw_body=command.raw_body,
            request_path=command.request_path,
            validator_dto=mappers.ConfigMapper.to_shipment_tracker_config_dto
        )

        # 4. Normalize the third-party schema into a generic internal DTO
        normalized_event_data: dtos.ShippingWebhookDTO = shipping_webhook_resolver.resolve(
            tenant_id=command.tenant_id,
            payload=validated_payload
        )

        # 5. Create an integration event DTO for the message bus
        integration_event = dtos.ShippingWebhookIntegrationEvent(
            event_type="shipping_tracker_webhook.received",
            data=normalized_event_data # Use the correct DTO variable name
        )

        # 6. Publish the event asynchronously for downstream consumers
        event_publisher.publish(integration_event)
        
        # In a command handler that doesn't modify local domain state, a UOW commit isn't needed.

        return dtos.ResponseDTO(
            success=True,
            message="Shipment updates have been published to queue."
        )

    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions (e.g., business logic validation errors)
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED/SYSTEM exceptions
        return exception_handler.handle_unexpected(e)

