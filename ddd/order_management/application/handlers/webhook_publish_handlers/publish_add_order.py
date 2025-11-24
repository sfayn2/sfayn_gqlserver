from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos,
    commands
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
        validated_payload: dict = webhook_receiver_service.validate(
            tenant_id=command.tenant_id, 
            headers=command.headers,
            raw_body=command.raw_body,
            request_path=command.request_path
        )

        # 3. Normalize the third-party schema into a generic internal DTO
        # This step maps the external format to your bounded context's ubiquitous language
        normalized_event_data: dtos.AddOrderDTO = dtos.AddOrderDTO(**json.loads(validated_payload['raw_body']))

        # 4. Create an integration event DTO for the message bus
        integration_event = dtos.AddOrderWebhookIntegrationEvent(
            event_type="add_order_webhook.received",
            data=normalized_event_data
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



