
from typing import Union
from ddd.order_management.application import unit_of_work, handlers, commands, queries
from ddd.order_management.domain import events

COMMAND_HANDLERS = {
    commands.PlaceOrderCommand: handlers.handle_place_order,
    commands.ConfirmOrderCommand: handlers.handle_confirm_order,
    commands.SelectShippingOptionCommand: handlers.handle_select_shipping_option,
    commands.CheckoutItemsCommand: handlers.handle_checkout_items,
}

QUERY_HANDLERS = {
    queries.ShippingOptionsQuery: handlers.handle_shipping_options
}

EVENT_HANDLERS = {
}

def handle(message: Union[commands.Command, queries.Query, events.DomainEvent], uow: unit_of_work.DjangoOrderUnitOfWork, dependencies: None):
    """ dispatch message to appropriate handler(s) """
    if isinstance(message, commands.Command):
        handler = COMMAND_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(message)}")
        results = handler(message, uow, **dependencies)
        return results
    elif isinstance(message, queries.Query):
        handler = QUERY_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for query: {type(message)}")
        results = handler(message, uow, **dependencies)
        return results
    elif isinstance(message, events.DomainEvent):
        handlers = EVENT_HANDLERS.get(type(message), [])
        for handler in handlers:
            handler(message, uow, **dependencies)
    else:
        raise ValueError(f"Unknown message type {type(message)}")

def publish(event, uow):
    #TODO how to pass dependencies like service?
    # handle the event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(type(event), [])
    for handler in handlers:
        handler(event, uow)

    # TODO?
    # publish the event  using the event publisher (Redis, Kafka, RabbitMQ, etc.?)