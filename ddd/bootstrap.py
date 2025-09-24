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
    email_senders,
    loggings,
    repositories,
    access_control1,
    snapshots,
    event_publishers,
    webhook_signatures,
    clocks,
    workflow
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

# Global clock; To evolve later on per tenant?
domain_services.DomainClock.configure(clocks.UTCClock())

# Configure Webhook Signature Verifier
application_services.webhook_validation_service.SIGNATURE_VERIFIER = {
    "wss": lambda tenant_id: webhook_signatures.WssSignatureVerifier(shared_secret=os.getenv(f"WH_SECRET_{tenant_id}"))
}

workflow_service = application_services.workflow_service.WorkflowService(
    workflow.DjangoWorkflowGateway(
        [
            dict(order_status=enums.OrderStatus.CONFIRMED, workflow_status="AddShipment", step_name="add_shipment", sequence=1, optional_step=False, conditions={}),
            dict(order_status=enums.OrderStatus.SHIPPED, workflow_status="Shipped", step_name="mark_as_shipped", sequence=2, optional_step=False, conditions={}),
            dict(order_status=enums.OrderStatus.SHIPPED, workflow_status="AddTrackingReference", step_name="add_shipping_tracking_reference", sequence=3, optional_step=False, conditions={}),
            dict(order_status=enums.OrderStatus.CANCELLED, workflow_status="Canceled", step_name="canceled_order", sequence=None, optional_step=False, conditions={}),
            dict(order_status=enums.OrderStatus.COMPLETED, workflow_status="Completed", step_name="mark_as_completed", sequence=4, optional_step=False, conditions={}),
        ]
    )
)

# Configure which events get published
event_bus.EXTERNAL_EVENT_WHITELIST = []
event_bus.INTERNAL_EVENT_WHITELIST = []

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
    "order_management.internal_events.TenantWorkflowUpdatedEvent": dtos.TenantWorkflowUpdateIntegrationEvent,
    "order_management.internal_events.TenantWorkflowUpdatedEvent": dtos.TenantRolemapUpdateIntegrationEvent,
    "order_management.internal_events.TenantWorkflowUpdatedEvent": dtos.TenantCreateOrderIntegrationEvent,
}


# External async (redis/kafka/etc) event handlers (from other services)
event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.update({
    "identity_gateway_service.external_events.UserLoggedInEvent": [
            lambda event: handlers.handle_user_logged_in_async_event(
                event=event,
                auth_snapshot_repo=snapshots.DjangoUserAuthorizationSnapshotRepo(),
                customer_snapshot_repo=snapshots.DjangoCustomerSnapshotRepo()
            ),
        ],
})


# Internal async (redis/kafka/etc?) event handlers (within this service)
event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.update({
    "order_management.internal_events.TenantWorkflowUpdatedEvent": [
        lambda event: handlers.handle_tenant_workflow_update_async_event(
            event=event,
            tenant_workflow_snapshot_repo=snapshots.DjangoVendorProductSnapshotRepo()
        ),
    ],
    "order_management.internal_events.TenantRolemapUpdatedEvent": [
        lambda event: handlers.handle_tenant_rolemap_update_async_event(
            event=event,
            tenant_rolemap_snapshot_repo=snapshots.DjangoVendorProductSnapshotRepo()
        ),
    ],
    "order_management.internal_events.TenantCreateOrderEvent": [
        lambda event: handlers.handle_tenant_create_order_async_event(
            event=event,
            tenant_create_order_snapshot_repo=snapshots.DjangoVendorProductSnapshotRepo()
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
})

# Command Handlers (write operations)
message_bus.COMMAND_HANDLERS.update({
    commands.ShipOrderCommand: lambda command, **deps: handlers.handle_mark_as_shipped(
        command=command,
        access_control=access_control,
        uow=repositories.DjangoOrderUnitOfWork(),
        workflow_service=workflow_service,
        **deps
    ),
    commands.AddShippingTrackingReferenceCommand: lambda command, **deps: handlers.handle_add_shipping_tracking_reference(
        command=command,
        access_control=access_control,
        uow=repositories.DjangoOrderUnitOfWork(),
        **deps
    ),
    commands.CompleteOrderCommand: lambda command, **deps: handlers.handle_mark_as_completed(
        command=command,
        access_control=access_control,
        uow=repositories.DjangoOrderUnitOfWork(),
        workflow_service=workflow_service,
        **deps
    ),
    **handlers.webhook_publish_command_handlers.get_command_handlers(commands, handlers, event_bus),
    **handlers.workflow_command_handlers.get_command_handlers(commands, handlers, repositories.DjangoOrderUnitOfWork(), access_control, workflow_service)
})

#Query Handlers (read operations)
message_bus.QUERY_HANDLERS.update({
    queries.GetOrderQuery: lambda query, **deps: handlers.handle_get_order(
        query=query, 
        uow=repositories.DjangoOrderUnitOfWork(),
        **deps
    ),
})
