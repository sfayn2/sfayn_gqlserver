
from ddd.order_management.domain import events
from ddd.order_management.infrastructure import event_bus
from ddd.order_management.infrastructure.adapters import (
    email_service, 
    logging_service
)
from ddd.order_management.application.handlers import (
    place_order,
    confirm_order,
    select_shipping_option,
    checkout_items,
    get_shipping_options,
    event_handlers
)

from ddd.order_management.application import commands, message_bus, queries


#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        events.OrderCancelled: [
            lambda event, uow: event_handlers.handle_logged_order(event, uow, logging_service=logging_service.LoggingService()),
            lambda event, uow: event_handlers.handle_email_canceled_order(event, uow, email_service=email_service.EmailService())
            ]
    })

def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.PlaceOrderCommand: place_order.handle_place_order,
        commands.ConfirmOrderCommand: confirm_order.handle_confirm_order,
        commands.SelectShippingOptionCommand: select_shipping_option.handle_select_shipping_option,
        commands.CheckoutItemsCommand: checkout_items.handle_checkout_items,
    })

def register_query_handlers():
    message_bus.QUERY_HANDLERS.update({
        queries.ShippingOptionsQuery: get_shipping_options.handle_shipping_options
    })