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
    repositories,
    access_control1,
    event_publishers,
    webhook_receiver,
    clocks,
    user_action_service,
    tenant_service,
    saas_service,
    shipping,
    exception_handler
)
from ddd.order_management.application import (
    handlers,
    commands, 
    message_bus, 
    queries,
    dtos,
    services as application_services
)

load_dotenv(find_dotenv(filename=".env.test"))

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
#if project grows, breakdown handlers by feature

# Moved to TenantRolePermissionSnapshot ==========
# Define role permissions
#ROLE_MAP = {
#    "vendor": ["oms.mark_as_shipped", "oms.add_shipping_tracking_reference", "oms.mark_as_completed", "oms.get_order"
#    "oms.escalate_reviewer", "oms.review_order", "oms.request_return", "oms.process_refund"],
#}
# ====================

saas_service_instance = saas_service.SaaSService()
tenant_service_instance = tenant_service.TenantService()

# ============== resolve access control based on tenant_id ===============
access_control1.AccessControlService.configure(
    saas_service=saas_service_instance,
    access_control_library=access_control1.AccessControl1,
    jwt_handler=access_control1.JwtTokenHandler
)


# =============== resolve shipping provider based on tenant_id ========
shipping.ShippingProviderService.configure(
    saas_service=saas_service_instance,
    shipping_provider_factory=shipping.ShippingProviderFactory
)

# ============== domain clock =============
domain_services.DomainClock.configure(clocks.UTCClock())

##================ logging ============
#loggings.LoggingService.configure(
#    loggings.StdLogProvider("tenant_oms_api")
#)

# ========= webhook receiver  =============
webhook_receiver.WebhookReceiverService.configure(
    saas_service=saas_service_instance,
    webhook_receiver_factory=webhook_receiver.WebhookReceiverFactory
)



# ============ Configure which events get published ===========
event_bus.EXTERNAL_EVENT_WHITELIST = []
event_bus.INTERNAL_EVENT_WHITELIST = []

# ===========Setup Redis event publishers ==========
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


#  ================ Map event types to validation models; define to support event payloads decoder w validation ============
event_bus.EVENT_MODELS = {}


# =========== External async (redis/kafka/etc) event handlers (from other services) =============
event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.update({
    "identity_gateway_service.external_events.UserLoggedInEvent": [
            lambda event: handlers.handle_user_logged_in_async_event(
                event=event,
                auth_snapshot_repo=snapshots.DjangoUserAuthorizationSnapshotRepo(),
                customer_snapshot_repo=snapshots.DjangoCustomerSnapshotRepo()
            ),
        ],
})


# ==================Internal async (redis/kafka/etc?) event handlers (within this service) ==================
event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.update({
    "order_management.internal_events.CreateOrderEvent": [
        lambda event: handlers.handle_create_order_async_event(
            event=event,
        ),
    ],
    "order_management.internal_events.ConfirmedShipmentEvent": [
        lambda event: handlers.handle_dispatch_shipment_async_event(
            event=event,
            user_action_service=user_action_service.UserActionService(),
            shipping_provider_service=shipping.ShippingProviderService,
            uow=repositories.DjangoOrderUnitOfWork()
        ),
    ],
})

# ======================= Domain event handlers (immediate processing) ==============
event_bus.EVENT_HANDLERS.update({
    events.CanceledOrderEvent: [
            lambda event, uow: handlers.handle_logged_order(
                event=event,
                uow=uow,
            ),
            lambda event, uow: handlers.handle_email_canceled_order(
                event=event, 
                uow=uow,
                email=email_sender.MyEmailSender()
            )
        ],
})

# =========== inject concrete impl / cross cutting =======================
message_bus.ACCESS_CONTROL_SERVICE_IMPL = access_control1.AccessControlService
#message_bus.LOGGING_SERVICE_IMPL = loggings.LoggingService
message_bus.EXCEPTION_HANDLER_FACTORY = exception_handler.OrderExceptionHandler
message_bus.UOW = repositories.DjangoOrderUnitOfWork()
message_bus.USER_ACTION_SERVICE_IMPL = user_action_service.UserActionService()

# ========= Command Handlers (write operations) ==================
message_bus.COMMAND_HANDLERS.update({
    commands.AddShipmentCommand: lambda command, **deps: handlers.handle_add_shipment(
        command=command,
        **deps
    ),
    commands.ConfirmShipmentCommand: lambda command, **deps: handlers.handle_confirm_shipment(
        command=command,
        shipping_provider_service=shipping.ShippingProviderService,
        **deps
    ),
    commands.AddShippingTrackingReferenceCommand: lambda command, **deps: handlers.handle_add_shipping_tracking_reference(
        command=command,
        **deps
    ),
    commands.DeliverShipmentCommand: lambda command, **deps: handlers.handle_deliver_shipment(
        command=command,
        **deps
    ),
    commands.CancelShipmentCommand: lambda command, **deps: handlers.handle_cancel_shipment(
        command=command,
        **deps
    ),
    commands.CancelOrderCommand: lambda command, **deps: handlers.handle_cancel_order(
        command=command,
        **deps
    ),
    commands.CompleteOrderCommand: lambda command, **deps: handlers.handle_mark_as_completed(
        command=command,
        **deps
    ),
    **handlers.webhook_publish_command_handlers.get_command_handlers(commands, handlers, event_bus),
    **handlers.user_action_command_handlers.get_command_handlers(commands, handlers, application_services, tenant_service)
})

# ================= Query Handlers (read operations) ===================
message_bus.QUERY_HANDLERS.update({
    queries.GetOrderQuery: lambda query, **deps: handlers.handle_get_order(
        query=query, 
        **deps
    ),
})
