
from ddd.order_management.domain import events, services
from ddd.order_management.infrastructure import event_bus, adapters
from ddd.order_management.application import handlers
from ddd.order_management.application.handlers import event_handlers

from ddd.order_management.application import commands, message_bus, queries

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        events.OrderCancelled: [
            lambda event, uow: event_handlers.handle_logged_order(event, uow, logging_service=adapters.LoggingService()),
            lambda event, uow: event_handlers.handle_email_canceled_order(event, uow, email_service=adapters.EmailService())
            ]
    })


def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.PlaceOrderCommand: handlers.handle_place_order,
        commands.ConfirmOrderCommand: lambda command, uow: handlers.handle_confirm_order(
            command, 
            uow,
            payment_gateway_factory=adapters.PaymentGatewayFactory(),
            order_service=services.OrderService(),
            tax_service=services.TaxStrategyService()
        ),
        commands.SelectShippingOptionCommand: lambda command, uow: handlers.handle_select_shipping_option(
            command, 
            uow,
            shipping_option_service=services.ShippingOptionStrategyService,
            order_service=services.OrderService()
        ),
        commands.CheckoutItemsCommand: lambda command, uow: handlers.handle_checkout_items(
            command,
            uow,
            order_service=services.OrderService(),
            tax_service=services.TaxStrategyService()
        ),
    })

def register_query_handlers():
    message_bus.QUERY_HANDLERS.update({
        queries.ShippingOptionsQuery: lambda query, uow: handlers.handle_shipping_options(
            query, 
            uow,
            shipping_option_service=services.ShippingOptionStrategyService,
            order_service=services.OrderService()
        ),
    })

def register():
    register_event_handlers()
    register_command_handlers
    register_query_handlers()