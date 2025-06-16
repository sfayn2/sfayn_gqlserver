
from ddd.order_management.domain import events, services as domain_services
from ddd.order_management.infrastructure import (
    event_bus, 
    validation_services, 
    email_services,
    logging_services,
    repositories,
    payment_services
)
from ddd.order_management.application import handlers
from ddd.order_management.application.handlers import event_handlers

from ddd.order_management.application import commands, message_bus, queries

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature


def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        "order_management.events.OrderCanceledEvent": [
                lambda event: handlers.handle_logged_order(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    logging=logging_services.LoggingService()
                ),
                lambda event: handlers.handle_email_canceled_order(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    email=email_services.EmailService()
                )
            ],
        "order_management.events.OrderPlacedEvent": [
                lambda event: handlers.handle_apply_applicable_offers(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    vendor=repositories.DjangoVendorRepositoryImpl(),
                    offer_service=domain_services.OfferStrategyService()
                )
            ],
        "order_management.events.OrderOffersAppliedEvent": [
                lambda event: handlers.handle_apply_tax_results(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    tax_service=domain_services.TaxStrategyService()
                )
            ],
        "order_management.events.OrderTaxesAppliedEvent": [
                lambda event: handlers.handle_logged_order(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    logging=logging_services.LoggingService()
                ),
            ],
        "order_management.events.OrderDraftEvent": [
                lambda event: handlers.handle_apply_tax_results(
                    event=event, 
                    uow=repositories.DjangoOrderUnitOfWork(),
                    tax_service=domain_services.TaxStrategyService()
                )
            ]
    })


def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.CheckoutItemsCommand: lambda command: handlers.handle_checkout_items(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            order_service=domain_services.OrderService(),
            product_vendor_validation_service=validation_services.DjangoProductsVendorValidationService()
        ),
        commands.SelectShippingOptionCommand: lambda command: handlers.handle_select_shipping_option(
            command=command, 
            uow=repositories.DjangoOrderUnitOfWork(),
            shipping_option_service=domain_services.ShippingOptionStrategyService
        ),
        commands.PlaceOrderCommand: lambda command: handlers.handle_place_order(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.ConfirmOrderCommand: lambda command: handlers.handle_confirm_order(
            command=command, 
            uow=repositories.DjangoOrderUnitOfWork(),
            payment_service=payment_services.PaymentService(),
            order_service=domain_services.OrderService(),
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.MarkAsShippedOrderCommand: lambda command: handlers.handle_mark_as_shipped(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.AddShippingTrackingReferenceCommand: lambda command: handlers.handle_add_shipping_tracking_reference(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.AddCouponCommand: lambda command: handlers.handle_add_coupon(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            coupon_validation=validation_services.DjangoCouponValidationService()
        ),
    })

def register_query_handlers():
    message_bus.QUERY_HANDLERS.update({
        queries.ShippingOptionsQuery: lambda query: handlers.handle_shipping_options(
            query=query, 
            uow=uow,
            shipping_option_service=domain_services.ShippingOptionStrategyService
        ),
    })

def register():
    register_event_handlers()
    register_command_handlers()
    register_query_handlers()