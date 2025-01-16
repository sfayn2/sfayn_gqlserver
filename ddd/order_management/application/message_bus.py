
from typing import Union
from ddd.order_management.application import unit_of_work, handlers, commands
from ddd.order_management.domain import events

COMMAND_HANDLERS = {
}

EVENT_HANDLERS = {
}

def handle(message: Union[commands.Command, events.DomainEvent], uow: unit_of_work.DjangoUnitOfWork):
    """ dispatch message to appropriate handler(s) """
    if isinstance(message, commands.Command):
        handler = COMMAND_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(message)}")
        event = handler(message, uow)
        handle_event(event, uow)
    elif isinstance(message, events.DomainEvent):
        handlers = EVENT_HANDLERS.get(type(message), [])
        for handler in handlers:
            handler(message, uow)
    else:
        raise ValueError(f"Unknown message type {type(message)}")

def handle_event(event, uow):
    # handle the event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(type(event), [])
    for handler in handlers:
        handler(event, uow)

    # TODO?
    # publish the event  using the event publisher (Redis, Kafka, RabbitMQ, etc.?)