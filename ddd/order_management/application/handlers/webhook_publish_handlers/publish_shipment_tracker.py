from __future__ import annotations
import json
import logging
from typing import Optional
from ddd.order_management.application import (
    ports, 
    dtos,
    commands,
    mappers
)
from ddd.order_management.domain import exceptions


def handle_publish_shipment_tracker(
    command: commands.PublishShipmentTrackerCommand, 
    uow: ports.UnitOfWorkAbstract,
    user_action_service: ports.UserActionServiceAbstract,
    exception_handler: ports.ExceptionHandlerAbstract,
    webhook_receiver_service: ports.WebhookReceiverServiceAbstract,
    shipment_lookup_service: ports.ShipmentLookupServiceAbstract,
    shipping_webhook_parser: ports.ShippingWebhookParserResolverAbstract,
    event_publisher: ports.EventPublisherAbstract,
    tracking_reference_extractor: ports.TrackingReferenceExtractorAbstract
) -> dtos.ResponseDTO:
    """
    Processes an incoming Shipping provider webhook request within a DDD context.
    """
    try:


        # 1. Extract the tracking reference from the raw request body
        tracking_reference = tracking_reference_extractor.extract_tracking_reference(
            command.raw_body, 

            #the name tenant_id is used here even if the command carries saas_id
            command.tenant_id
        )
        
        # 2. Identify the tenant associated with the shipment tracking reference
        context: Optional[dtos.ShipmentLookupContextDTO] = shipment_lookup_service.get_context_by_tracking_ref(tracking_reference)

        if not context:
            # Raise an explicit domain exception if we cannot route the webhook
            raise exceptions.InvalidOrderOperation(
                f"No shipment found for tracking reference {tracking_reference}. Cannot process webhook."
            )
        
        # 3. Validate the raw payload signature/origin using tenant-specific credentials
        webhook_receiver_service.validate_signature(
            tenant_id=context.tenant_id,
            headers=command.headers,
            raw_body=command.raw_body,
            request_path=command.request_path,
            validator_dto=mappers.ConfigMapper.to_shipment_tracker_config_dto
        )

        # 4. Normalize the third-party schema into a generic internal DTO
        normalized_dto: dtos.ShippingWebhookRequestDTO = shipping_webhook_parser.parse(
            tenant_id=context.tenant_id,
            order_id=context.order_id,
            raw_body=command.raw_body
        )

        # 5. Create an integration event DTO for the message bus
        integration_event = dtos.ShippingWebhookIntegrationEvent(
            event_type=dtos.IntegrationEventType.SHIPPING_TRACKER_WEBHOOK_RECEIVED,
            data=normalized_dto # Use the correct DTO variable name
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

