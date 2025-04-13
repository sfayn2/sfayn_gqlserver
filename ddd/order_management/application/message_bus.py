
from typing import Union
from ddd.order_management.application import commands, handlers1, queries
from ddd.order_management.application.handlers import (
    place_order,
    confirm_order,
    select_shipping_option,
    checkout_items,
    get_shipping_options
)
from ddd.order_management.domain import repositories


COMMAND_HANDLERS = {
    commands.PlaceOrderCommand: place_order.handle_place_order,
    commands.ConfirmOrderCommand: confirm_order.handle_confirm_order,
    commands.SelectShippingOptionCommand: select_shipping_option.handle_select_shipping_option,
    commands.CheckoutItemsCommand: checkout_items.handle_checkout_items,
}

QUERY_HANDLERS = {
    queries.ShippingOptionsQuery: get_shipping_options.handle_shipping_options
}


def handle(message: Union[commands.Command, queries.Query], uow: repositories.UnitOfWorkAbstract, dependencies: None):
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
    else:
        raise ValueError(f"Unknown message type {type(message)}")
