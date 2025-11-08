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
    exception_handler: ports.ExceptionHandlerAbstract,
    event_publisher: ports.EventPublisherAbstract
):
    try:
        event = dtos.AddOrderIntegrationEvent(
            **command.model_dump()
        )

        event_publisher.publish(event)

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



