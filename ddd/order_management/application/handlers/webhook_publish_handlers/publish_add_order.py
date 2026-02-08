from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos,
    commands,
    mappers
)
from ddd.order_management.domain import events, exceptions

def handle_publish_add_order(
    command: commands.PublishAddOrderCommand, 
    uow: ports.UnitOfWorkAbstract,
    exception_handler: ports.ExceptionHandlerAbstract,
    webhook_receiver_service: ports.WebhookReceiverServiceAbstract,
    user_action_service: ports.UserActionServiceAbstract,
    event_publisher: ports.EventPublisherAbstract
):
    try:

        # 2. Validate the raw payload with the external service
        # The service is responsible for signature checks, schema validation, etc.
        webhook_receiver_service.validate_signature(
            tenant_id=command.tenant_id, 
            headers=command.headers,
            raw_body=command.raw_body,
            request_path=command.request_path,
            validator_dto=mappers.ConfigMapper.to_add_order_config_dto
        )

        
        # 4. Create an integration event DTO for the message bus
        integration_event = dtos.AddOrderWebhookIntegrationEvent(
            event_type=dtos.IntegrationEventType.ADD_ORDER_WEBHOOK_RECEIVED,

            # phase1: If external want to create an order in our system via webhook, they must send it in this specific contract AddOrderIntegrationDTO.
            # phase2: we allow the customer to just "point" their Shopify/Magento webhook at our URL, and  system (the Resolver/Translator) does the work for them
            data=dtos.AddOrderIntegrationDTO(**webhook_receiver_service.get_payload(
                raw_body=command.raw_body
            ))
        )

        # 5. Publish the event asynchronously for downstream consumers
        event_publisher.publish(integration_event)

        return dtos.ResponseDTO(
            success=True,
            message="New order has been publish to queue."
        )

    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)



