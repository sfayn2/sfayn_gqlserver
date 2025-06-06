
from ddd.order_management.domain import events, services
from ddd.order_management.infrastructure import event_bus, adapters
from ddd.order_management.application import handlers
from ddd.order_management.application.handlers import event_handlers

from ddd.order_management.application import commands, message_bus, queries

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        events.OrderCanceledEvent: [
                lambda event, uow: handlers.handle_logged_order(
                    event=event, 
                    uow=uow, 
                    logging=adapters.LoggingAdapter()
                ),
                lambda event, uow: handlers.handle_email_canceled_order(
                    event=event, 
                    uow=uow, 
                    email=adapters.EmailAdapter()
                )
            ],
        events.OrderPlacedEvent: [
                lambda event, uow: handlers.handle_apply_applicable_offers(
                    event=event, 
                    uow=uow, 
                    offer_service=services.OfferStrategyService(uow.vendor)
                )
            ],
        events.OfferAppliedEvent: [
                lambda event, uow: handlers.handle_apply_tax_results(
                    event=event, 
                    uow=uow, 
                    tax_service=services.TaxStrategyService()
                )
            ],
        events.OrderDraftEvent: [
                lambda event, uow: handlers.handle_apply_tax_results(
                    event=event, 
                    uow=uow, 
                    tax_service=services.TaxStrategyService()
                )
            ]
    })


def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.CheckoutItemsCommand: lambda command, uow: handlers.handle_checkout_items(
            command=command,
            uow=uow,
            order_service=services.OrderService(),
            product_vendor_validation_service=adapters.ProductVendorValidationServiceAdapter()
        ),
        commands.SelectShippingOptionCommand: lambda command, uow: handlers.handle_select_shipping_option(
            command=command, 
            uow=uow,
            shipping_option_service=services.ShippingOptionStrategyService
        ),
        commands.PlaceOrderCommand: lambda command, uow: handlers.handle_place_order(
            command=command,
            uow=uow,
            stock_validation_service=adapters.DjangoStockValidationServiceAdapter()
        ),
        commands.ConfirmOrderCommand: lambda command, uow: handlers.handle_confirm_order(
            command=command, 
            uow=uow,
            payment_gateway_factory=adapters.PaymentGatewayFactoryAdapter(),
            order_service=services.OrderService(),
            stock_validation_service=adapters.DjangoStockValidationServiceAdapter()
        ),
        commands.MarkAsShippedOrderCommand: lambda command, uow: handlers.handle_mark_as_shipped(
            command=command,
            uow=uow
        ),
        commands.AddShippingTrackingReferenceCommand: lambda command, uow: handlers.handle_add_shipping_tracking_reference(
            command=command,
            uow=uow
        ),
        commands.AddCouponCommand: lambda command, uow: handlers.handle_add_coupon(
            command=command,
            uow=uow,
            coupon_validation=adapters.DjangoCouponValidationAdapter()
        ),
    })

def register_query_handlers():
    message_bus.QUERY_HANDLERS.update({
        queries.ShippingOptionsQuery: lambda query, uow: handlers.handle_shipping_options(
            query=query, 
            uow=uow,
            shipping_option_service=services.ShippingOptionStrategyService
        ),
    })

def register():
    register_event_handlers()
    register_command_handlers()
    register_query_handlers()