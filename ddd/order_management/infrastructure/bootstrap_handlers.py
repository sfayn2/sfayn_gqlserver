import os
from dotenv import load_dotenv
from ddd.order_management.domain import events, services as domain_services
from ddd.order_management.infrastructure import (
    event_bus, 
    validation_services, 
    email_services,
    logging_services,
    repositories,
    payment_services,
    idp_services,
    access_control_services,
    snapshot_services
)
from ddd.order_management.application import handlers
from ddd.order_management.application.handlers import event_handlers

from ddd.order_management.application import commands, message_bus, queries

load_dotenv()

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

role_map = {
    "customer": ["checkout_items", "add_line_items", "remove_line_items", 
    "add_coupon", "remove_coupon", "change_destination", "change_order_quantity", 
    "select_shipping_option", "list_shipping_options", "list_customer_addresses"
    "place_order", "confirm_order", "cancel_order", "get_order"],
    "vendor": ["mark_as_shipped", "add_shipping_tracking_reference", "mark_as_completed"]
}

# ===============================
#TODO to have this in separate auth_service
# =====================
jwt_handler = access_control_services.JwtTokenHandler(
    public_key=os.getenv("KEYCLOAK_PUBLIC_KEY"),
    issuer=os.getenv("KEYCLOAK_ISSUER"),
    audience=os.getenv("KEYCLOAK_CLIENT_ID")
)


idp_provider = idp_services.KeycloakIdPProvider(
    token_url=os.getenv("KEYCLOAK_TOKEN"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET")
)

login_callback_service = idp_services.KeycloakLoginCallbackService(
    idp_provider=idp_provider,
    jwt_handler=jwt_handler,
    role_map=role_map
)
# ===============================
#TODO to have this in separate auth_service
# =====================

access_control = access_control_services.AccessControlService(
    jwt_handler=jwt_handler
)

def register_async_event_handlers():
    event_bus.ASYNC_EVENT_HANDLERS.update({
        "auth_service.events.UserLoggedInEvent": [
                lambda event: handlers.handle_user_logged_in(
                    event=event,
                    auth_sync=snapshot_services.DjangoUserAuthorizationSnapshotSyncService(role_map),
                    customer_sync=snapshot_services.DjangoCustomerSnapshotSyncService()
                ),
            ],
    })


def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        "order_management.events.CanceledOrderEvent": [
                lambda event, uow: handlers.handle_logged_order(
                    event=event,
                    uow=uow,
                    logging=logging_services.LoggingService()
                ),
                lambda event, uow: handlers.handle_email_canceled_order(
                    event=event, 
                    uow=uow,
                    email=email_services.EmailService()
                )
            ],
        "order_management.events.OrderShippingOptionSelectedEvent": [
                lambda event, uow: handlers.handle_apply_applicable_offers(
                    event=event, 
                    uow=uow,
                    vendor=repositories.DjangoVendorRepositoryImpl(),
                    offer_service=domain_services.OfferStrategyService()
                )
            ],
        "order_management.events.OrderOffersAppliedEvent": [
                lambda event, uow: handlers.handle_apply_tax_results(
                    event=event, 
                    uow=uow,
                    tax_service=domain_services.TaxStrategyService()
                )
            ],
        "order_management.events.OrderTaxesAppliedEvent": [
                lambda event, uow: handlers.handle_logged_order(
                    event=event, 
                    uow=uow,
                    logging=logging_services.LoggingService()
                ),
            ],
    })


def register_command_handlers():
    message_bus.COMMAND_HANDLERS.update({
        commands.CheckoutItemsCommand: lambda command: handlers.handle_checkout_items(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            customer_repo=repositories.DjangoCustomerRepositoryImpl(),
            vendor_repo=repositories.DjangoVendorRepositoryImpl(),
            order_service=domain_services.OrderService(),
            address_validation_service=validation_services.DjangoCustomerAddressValidationService(),
            stock_validation_service=validation_services.DjangoStockValidationService(),
            access_control=access_control
        ),
        commands.ChangeOrderQuantityCommand: lambda command: handlers.handle_change_order_quantity(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.AddLineItemsCommand: lambda command: handlers.handle_add_line_items(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            vendor_repo=repositories.DjangoVendorRepositoryImpl(),
            access_control=access_control,
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.ChangeDestinationCommand: lambda command: handlers.handle_change_destination(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            validation_service=validation_services.DjangoCustomerAddressValidationService()
        ),
        commands.AddCouponCommand: lambda command: handlers.handle_add_coupon(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            coupon_validation_service=validation_services.DjangoCouponValidationService(),
            access_control=access_control
        ),
        commands.SelectShippingOptionCommand: lambda command: handlers.handle_select_shipping_option(
            command=command, 
            uow=repositories.DjangoOrderUnitOfWork(),
            vendor_repo=repositories.DjangoVendorRepositoryImpl(),
            access_control=access_control,
            shipping_option_service=domain_services.ShippingOptionStrategyService()
        ),
        commands.PlaceOrderCommand: lambda command: handlers.handle_place_order(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            access_control=access_control,
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.ConfirmOrderCommand: lambda command: handlers.handle_confirm_order(
            command=command, 
            uow=repositories.DjangoOrderUnitOfWork(),
            payment_service=payment_services.PaymentService(),
            access_control=access_control,
            stock_validation_service=validation_services.DjangoStockValidationService()
        ),
        commands.CancelOrderCommand: lambda command: handlers.handle_cancel_order(
            command=command,
            access_control=access_control,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.ShipOrderCommand: lambda command: handlers.handle_mark_as_shipped(
            command=command,
            access_control=access_control,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.AddShippingTrackingReferenceCommand: lambda command: handlers.handle_add_shipping_tracking_reference(
            command=command,
            access_control=access_control,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.CompleteOrderCommand: lambda command: handlers.handle_mark_as_completed(
            command=command,
            access_control=access_control,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
        commands.LoginCallbackCommand: lambda command: handlers.handle_login_callback(
            command=command,
            uow=repositories.DjangoOrderUnitOfWork(),
            login_callback_service=login_callback_service
        ),
    })

def register_query_handlers():
    message_bus.QUERY_HANDLERS.update({
        queries.ListShippingOptionsQuery: lambda query: handlers.handle_list_shipping_options(
            query=query, 
            uow=repositories.DjangoOrderUnitOfWork(),
            vendor_repo=repositories.DjangoVendorRepositoryImpl(),
            shipping_option_service=domain_services.ShippingOptionStrategyService()
        ),
        queries.ListCustomerAddressesQuery: lambda query: handlers.handle_list_customer_addresses(
            query=query, 
            uow=repositories.DjangoOrderUnitOfWork(),
            customer_repo=repositories.DjangoCustomerRepositoryImpl()
        ),
        queries.GetOrderQuery: lambda query: handlers.handle_get_order(
            query=query, 
            uow=repositories.DjangoOrderUnitOfWork()
        ),
    })

def register():
    register_event_handlers()
    register_async_event_handlers()

    register_command_handlers()
    register_query_handlers()