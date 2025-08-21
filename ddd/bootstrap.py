import os, redis
from dotenv import load_dotenv, find_dotenv
from ddd.order_management.domain import (
    events, 
    enums, 
    value_objects,
    services as domain_services
)
from ddd.order_management.infrastructure import (
    event_bus, 
    validations, 
    email_senders,
    loggings,
    repositories,
    access_control1,
    snapshots,
    event_publishers,
    payment_gateways,
    webhook_signatures
)
from ddd.order_management.application import (
    handlers,
    commands, 
    message_bus, 
    queries,
    dtos,
    services as application_services
)
from ddd.order_management.application.services import (
    webhook_validation_service,
    payment_service,
    shipping_option_service
)

load_dotenv(find_dotenv(filename=".env.test"))

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

# Define role permissions
ROLE_MAP = {
    "customer": ["checkout_items", "add_line_items", "remove_line_items", 
    "add_coupon", "remove_coupon", "change_destination", "change_order_quantity", 
    "select_shipping_option", "list_shipping_options", "list_customer_addresses"
    "place_order", "confirm_order", "cancel_order", "get_order"],
    "vendor": ["mark_as_shipped", "add_shipping_tracking_reference", "mark_as_completed"]
}

# JWT handler for access acontrol
JWT_HANDLER = access_control1.JwtTokenHandler(
    public_key=os.getenv("KEYCLOAK_PUBLIC_KEY"),
    issuer=os.getenv("KEYCLOAK_ISSUER"),
    audience=os.getenv("KEYCLOAK_CLIENT_ID"),
    algorithm=os.getenv("KEYCLOAK_ALGORITHM")
)

# Configure JWT Authentication
access_control = access_control1.AccessControl1(
    jwt_handler=JWT_HANDLER
)


# Configure supported shipping options (if eligible)
shipping_option_service.SHIPPING_OPTIONS = [
    (enums.ShippingMethod.STANDARD, domain_services.shipping_option_strategies.StandardShippingStrategy),
    (enums.ShippingMethod.EXPRESS, domain_services.shipping_option_strategies.ExpressShippingStrategy),
    (enums.ShippingMethod.LOCAL_PICKUP, domain_services.shipping_option_strategies.LocalPickupShippingStrategy),
    (enums.ShippingMethod.FREE_SHIPPING, domain_services.shipping_option_strategies.FreeShippingStrategy),

    #(enums.ShippingMethod.STANDARD, "Custom also can?")
    #(enums.ShippingMethod.OTHER, "Custom here?")
]

# Configure supported payment gateways
payment_service.PAYMENT_GATEWAYS = {
    enums.PaymentMethod.PAYPAL: payment_gateways.PaypalPaymentGateway(),
    enums.PaymentMethod.STRIPE: payment_gateways.StripePaymentGateway()
}

# Configure Webhook Signature Verifier
webhook_validation_service.SIGNATURE_VERIFIER = {
    "wss": lambda tenant_id: webhook_signatures.WssSignatureVerifier(shared_secret=os.getenv(f"WH_SECRET_{tenant_id}"))
}

# Configure which events get published
event_bus.EXTERNAL_EVENT_WHITELIST = []
event_bus.INTERNAL_EVENT_WHITELIST = [
    "order_management.internal_events.ProductUpdatedEvent",
    "order_management.internal_events.VendorDetailsUpdatedEvent",
    "order_management.internal_events.VendorCouponUpdatedEvent",
    "order_management.internal_events.VendorOfferUpdatedEvent",
    "order_management.internal_events.VendorShippingOptionUpdatedEvent"
]

# Setup Redis event publishers
event_bus.internal_publisher = event_publishers.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(os.getenv("REDIS_INTERNAL_URL"), decode_responses=True),
            stream_name=os.getenv("REDIS_INTERNAL_STREAM"),
            event_whitelist=event_bus.INTERNAL_EVENT_WHITELIST
        )
event_bus.external_publisher = event_publishers.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(os.getenv("REDIS_EXTERNAL_URL"), decode_responses=True),
            stream_name=os.getenv("REDIS_EXTERNAL_STREAM"),
            event_whitelist=event_bus.EXTERNAL_EVENT_WHITELIST
        )


# Map event types to validation models; define to support event payloads decoder w validation
event_bus.EVENT_MODELS = {
    "order_management.internal_events.ProductUpdatedEvent": dtos.ProductUpdateIntegrationEvent,
    "order_management.internal_events.VendorDetailsUpdatedEvent": dtos.VendorDetailsUpdateIntegrationEvent,
    "order_management.internal_events.VendorCouponUpdatedEvent": dtos.VendorCouponUpdateIntegrationEvent,
    "order_management.internal_events.VendorOfferUpdatedEvent": dtos.VendorOfferUpdateIntegrationEvent,
    "order_management.internal_events.VendorShippingOptionUpdatedEvent": dtos.VendorShippingOptionUpdateIntegrationEvent
}


# External async (redis/kafka/etc) event handlers (from other services)
event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.update({
    "identity_gateway_service.external_events.UserLoggedInEvent": [
            lambda event: handlers.handle_user_logged_in_async_event(
                event=event,
                auth_snapshot_repo=snapshots.DjangoUserAuthorizationSnapshotRepo(ROLE_MAP),
                customer_snapshot_repo=snapshots.DjangoCustomerSnapshotRepo()
            ),
        ],
    "product_catalog.external_events.ProductUpdatedEvent": [],
    "vendor_registry.external_events.VendorUpdatedEvent":[],
    "vendor_registry.external_events.VendorOfferUpdatedEvent":[],
    "vendor_registry.external_events.VendorShippingOptionUpdatedEvent":[]
})


# Internal async (redis/kafka/etc?) event handlers (within this service)
event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.update({
    "order_management.internal_events.ProductUpdatedEvent": [
        lambda event: handlers.handle_product_update_async_event(
            event=event,
            product_snapshot_repo=snapshots.DjangoVendorProductSnapshotRepo()
        ),
    ],
    "order_management.internal_events.VendorDetailsUpdatedEvent": [
        lambda event: handlers.handle_vendor_details_update_async_event(
            event=event,
            vendor_details_snapshot_repo=snapshots.DjangoVendorDetailsSnapshotRepo()
        ),
    ],
    "order_management.internal_events.VendorCouponUpdatedEvent": [
        lambda event: handlers.handle_vendor_coupon_update_async_event(
            event=event,
            vendor_coupon_snapshot_repo=snapshots.DjangoVendorCouponSnapshotRepo()
        ),
    ],
    "order_management.internal_events.VendorOfferUpdatedEvent": [
        lambda event: handlers.handle_vendor_offer_update_async_event(
            event=event,
            vendor_offer_snapshot_repo=snapshots.DjangoVendorOfferSnapshotRepo()
        ),
    ],
    "order_management.internal_events.VendorShippingOptionUpdatedEvent": [
        lambda event: handlers.handle_vendor_shippingoption_update_async_event(
            event=event,
            vendor_shippingoption_snapshot_repo=snapshots.DjangoVendorShippingOptionSnapshotRepo()
        ),
    ],
})

# Domain event handlers (immediate processing)
event_bus.EVENT_HANDLERS.update({
    events.CanceledOrderEvent: [
            lambda event, uow: handlers.handle_logged_order(
                event=event,
                uow=uow,
                logging=loggings.SampleLogging()
            ),
            lambda event, uow: handlers.handle_email_canceled_order(
                event=event, 
                uow=uow,
                email=email_sender.MyEmailSender()
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
                logging=loggings.SampleLogging()
            ),
        ],
})

# Command Handlers (write operations)
message_bus.COMMAND_HANDLERS.update({
    commands.CheckoutItemsCommand: lambda command: handlers.handle_checkout_items(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        vendor_repo=repositories.DjangoVendorRepositoryImpl(),
        order_service=domain_services.OrderService(),
        address_validation_service=validation_services.DjangoCustomerAddressValidationService(),
        stock_validation=validation_services.DjangoStockValidationService(),
        access_control=access_control
    ),
    commands.ChangeOrderQuantityCommand: lambda command: handlers.handle_change_order_quantity(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        access_control=access_control,
        stock_validation=validation_services.DjangoStockValidationService()
    ),
    commands.AddLineItemsCommand: lambda command: handlers.handle_add_line_items(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        vendor_repo=repositories.DjangoVendorRepositoryImpl(),
        access_control=access_control,
        stock_validation=validation_services.DjangoStockValidationService()
    ),
    commands.ChangeDestinationCommand: lambda command: handlers.handle_change_destination(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        access_control=access_control
    ),
    commands.AddCouponCommand: lambda command: handlers.handle_add_coupon(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        coupon_validation=validation_services.DjangoCouponValidationService(),
        access_control=access_control
    ),
    commands.SelectShippingOptionCommand: lambda command: handlers.handle_select_shipping_option(
        command=command, 
        uow=repositories.DjangoOrderUnitOfWork(),
        vendor_repo=repositories.DjangoVendorRepositoryImpl(),
        access_control=access_control,
        shipping_option_service=shipping_option_service.ShippingOptionStrategyService()
    ),
    commands.PlaceOrderCommand: lambda command: handlers.handle_place_order(
        command=command,
        uow=repositories.DjangoOrderUnitOfWork(),
        access_control=access_control,
        stock_validation=validation_services.DjangoStockValidationService()
    ),
    commands.ConfirmOrderCommand: lambda command: handlers.handle_confirm_order(
        command=command, 
        uow=repositories.DjangoOrderUnitOfWork(),
        payment_service=application_services.PaymentService(),
        access_control=access_control,
        stock_validation=validation_services.DjangoStockValidationService()
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
    ),
    commands.PublishVendorDetailsUpdateCommand: lambda command: handlers.handle_publish_vendor_details_update(
        command=command,
        event_publisher=event_bus.internal_publisher
    ),
    commands.PublishVendorCouponUpdateCommand: lambda command: handlers.handle_publish_vendor_coupon_update(
        command=command,
        event_publisher=event_bus.internal_publisher
    ),
    commands.PublishVendorOfferUpdateCommand: lambda command: handlers.handle_publish_vendor_offer_update(
        command=command,
        event_publisher=event_bus.internal_publisher
    ),
    commands.PublishVendorShippingOptionUpdateCommand: lambda command: handlers.handle_publish_vendor_shippingoption_update(
        command=command,
        event_publisher=event_bus.internal_publisher
    )
})

#Query Handlers (read operations)
message_bus.QUERY_HANDLERS.update({
    queries.ListShippingOptionsQuery: lambda query: handlers.handle_list_shipping_options(
        query=query, 
        uow=repositories.DjangoOrderUnitOfWork(),
        vendor_repo=repositories.DjangoVendorRepositoryImpl(),
        shipping_option_service=shipping_option_service.ShippingOptionStrategyService()
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
