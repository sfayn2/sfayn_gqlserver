from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos,
    commands
)
from ddd.order_management.domain import events, exceptions

def handle_publish_shipment_updates(
    command: commands.PublishShipmentUpdatesCommand, 
    uow: ports.UnitOfWorkAbstract,
    exception_handler: ports.ExceptionHandlerAbstract,
    user_action_service: ports.UserActionServiceAbstract,
    shipping_webhook_resover: ports.ShippingWebhookResolverAbstract,
    event_publisher: ports.EventPublisherAbstract
):
    try:
        tenant_id = command.payload["metadata"]["tenant_id"]
        normalized_event_data = shipping_webhook_resolver.resolve(
            tenant_id=tenant_id,
            payload=command.data.payload,
        )

        event = dtos.ShippingWebhookIntegrationEvent(
            **normalized_event_data
        )

        event_publisher.publish(event)

        return dtos.ResponseDTO(
            success=True,
            message="Shipment updats has been publish to queue."
        )

    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)



