import os, redis
from dotenv import load_dotenv, find_dotenv
from ddd.order_management.domain import events, services as domain_services
from ddd.order_management.infrastructure import (
    event_bus, 
    validation_services, 
    email_services,
    logging_services,
    repositories,
    payment_services,
    access_control_services,
    snapshot_services,
    event_publishers
)
from ddd.order_management.application import (
    handlers,
    commands, 
    message_bus, 
    queries,
    dtos
)

load_dotenv(find_dotenv(filename=".env.test"))

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

# Gives more control by assigning default permission based on role
ROLE_MAP = {
    "customer": ["checkout_items", "add_line_items", "remove_line_items", 
    "add_coupon", "remove_coupon", "change_destination", "change_order_quantity", 
    "select_shipping_option", "list_shipping_options", "list_customer_addresses"
    "place_order", "confirm_order", "cancel_order", "get_order"],
    "vendor": ["mark_as_shipped", "add_shipping_tracking_reference", "mark_as_completed"]
}

# JWT handler for access acontrol
JWT_HANDLER = access_control_services.JwtTokenHandler(
    public_key=os.getenv("KEYCLOAK_PUBLIC_KEY"),
    issuer=os.getenv("KEYCLOAK_ISSUER"),
    audience=os.getenv("KEYCLOAK_CLIENT_ID"),
    algorithm=os.getenv("KEYCLOAK_ALGORITHM")
)

# Set access control
access_control = access_control_services.AccessControlService(
    jwt_handler=JWT_HANDLER
)

# Gives more control which event/s to publish externally
event_bus.EXTERNAL_EVENT_WHITELIST = []

# Gives more control which event/s to publish internallternally
event_bus.INTERNAL_EVENT_WHITELIST = [
    "order_management.internal_events.ProductUpdatedEvent",
]

# Set internal publisher eg. Redis/Kafka/etc
event_bus.internal_publisher = event_publishers.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(os.getenv("REDIS_INTERNAL_URL"), decode_responses=True),
            stream_name=os.getenv("REDIS_INTERNAL_STREAM"),
            event_whitelist=event_bus.INTERNAL_EVENT_WHITELIST
        )

# Set external publisher eg. Redis/Kafka/etc
event_bus.external_publisher = event_publishers.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(os.getenv("REDIS_EXTERNAL_URL"), decode_responses=True),
            stream_name=os.getenv("REDIS_EXTERNAL_STREAM"),
            event_whitelist=event_bus.EXTERNAL_EVENT_WHITELIST
        )


# Set central mapping of models used to validate event payloads based on even type
event_bus.EVENT_MODELS = {
    "order_management.internal_events.ProductUpdatedEvent": dtos.ProductUpdateIntegrationEvent
}


# Async Event handlers from External system / Redis;kafka stream
event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.update({
    "identity_gateway_service.external_events.UserLoggedInEvent": [
            lambda event: handlers.handle_user_logged_in_async_event(
                event=event,
                auth_sync=snapshot_services.DjangoUserAuthorizationSnapshotSyncService(ROLE_MAP),
                customer_sync=snapshot_services.DjangoCustomerSnapshotSyncService()
            ),
        ],
    "product_catalog.external_events.ProductUpdatedEvent": [],
    "vendor_registry.external_events.VendorUpdatedEvent":[],
    "vendor_registry.external_events.VendorOfferUpdatedEvent":[],
    "vendor_registry.external_events.VendorShippingOptionUpdatedEvent":[]
})


# Async Event handlers from Internal system / Redis;kafka stream
event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.update({
    "order_management.internal_events.ProductUpdatedEvent": [
        lambda event: handlers.handle_product_update_async_event(
            event=event,
            product_sync=snapshot_services.DjangoVendorProductSnapshotSyncService()
        ),
    ],
})

# Sync Event handlers from Internal domain event
event_bus.EVENT_HANDLERS.update({
    events.CanceledOrderEvent: [
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
    events.SelectedShippingOptionEvent: [
            lambda event, uow: handlers.handle_apply_applicable_offers(
                event=event, 
                uow=uow,
                vendor=repositories.DjangoVendorRepositoryImpl(),
                offer_service=domain_services.OfferStrategyService()
            )
        ],
    events.AppliedOffersEvent: [
            lambda event, uow: handlers.handle_apply_tax_results(
                event=event, 
                uow=uow,
                tax_service=domain_services.TaxStrategyService()
            )
        ],
    events.AppliedTaxesEvent: [
            lambda event, uow: handlers.handle_logged_order(
                event=event, 
                uow=uow,
                logging=logging_services.LoggingService()
            ),
        ],
})

# Command Handlers
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
    commands.PublishProductUpdateCommand: lambda command: handlers.handle_publish_product_update(
        command=command,
        event_publisher=event_bus.internal_publisher
    )
})

#Query Handlers
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
