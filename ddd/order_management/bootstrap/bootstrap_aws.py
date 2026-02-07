import os
from dotenv import load_dotenv, find_dotenv
from ddd.order_management.domain import (
    events, 
    enums, 
    value_objects,
    services as domain_services
)
from ddd.order_management.infrastructure import (
    event_bus,
    header_extractor, 
    repositories,
    access_control1,
    event_publishers,
    webhook_receiver,
    clocks,
    user_action_service,
    tenant_lookup_service,
    saas_lookup_service,
    shipping,
    shipping_webhook_parser,
    shipment_lookup_service,
    exception_handler,
    header_extractor,
    tracking_reference_extractor
)
from ddd.order_management.application import (
    handlers,
    commands, 
    message_bus, 
    queries,
    dtos,
    services as application_services
)

# entrypoint imports
from ddd.order_management.entrypoints.graphql.common import  (
    GraphqlContext
)

def bootstrap_aws():
    """
    Bootstrap configuration for AWS Lambda environment.
    This sets up all necessary service implementations and configurations
    specific to AWS infrastructure.
    """


    # Not applicable for AWS Lambda has its own env mgmt
    #load_dotenv(find_dotenv(filename=".env.aws.test"))

    #Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
    #if project grows, breakdown handlers by feature

    # Moved to TenantRolePermissionSnapshot ==========
    # Define role permissions
    #ROLE_MAP = {
    #    "vendor": ["oms.mark_as_shipped", "oms.add_shipping_tracking_reference", "oms.mark_as_completed", "oms.get_order"
    #    "oms.escalate_reviewer", "oms.review_order", "oms.request_return", "oms.process_refund"],
    #}
    # ====================
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "tenantoms_db")

    saas_lookup_service_instance = saas_lookup_service.DynamodbSaaSLookupService(table_name=DYNAMODB_TABLE_NAME)
    tenant_lookup_service_instance = tenant_lookup_service.DynamodbTenantLookupService(table_name=DYNAMODB_TABLE_NAME)


    # ============== configure entrypoints GraphQL context resolver ==================
    GraphqlContext.configure(
        saas_lookup_service=saas_lookup_service_instance,
        header_extractor=header_extractor.APIGatewayHeaderExtractor()
    )

    # ============== resolve access control based on tenant_id ===============
    access_control1.AccessControlService.configure(
        saas_lookup_service=saas_lookup_service_instance,
        access_control_library=access_control1.DynamodbAccessControl1,
        jwt_handler=access_control1.JwtTokenHandler
    )


    # =============== resolve shipping provider based on tenant_id ========
    shipping.ShippingProviderService.configure(
        saas_lookup_service=saas_lookup_service_instance,
        tenant_lookup_service=tenant_lookup_service_instance,
        shipping_provider_factory=shipping.ShippingProviderFactory()
    )

    # =============== resolve shipping webhook parser based on tenant_id ========
    shipping_webhook_parser.ShippingWebhookParserResolver.configure(
        saas_lookup_service=saas_lookup_service_instance,
        tenant_lookup_service=tenant_lookup_service_instance,
        shipping_parser_factory=shipping_webhook_parser.ShippingWebhookParserFactory()
    )

    # =============== resolve tracking reference extractor based on saas_id ========
    tracking_reference_extractor.TrackingReferenceExtractor.configure(
        saas_lookup_service=saas_lookup_service_instance
    )

    # ============== domain clock =============
    domain_services.DomainClock.configure(clocks.UTCClock())

    ##================ logging ============
    #loggings.LoggingService.configure(
    #    loggings.StdLogProvider("tenant_oms_api")
    #)

    # ========= webhook receiver  =============
    webhook_receiver.WebhookReceiverService.configure(
        saas_lookup_service=saas_lookup_service_instance,
        tenant_lookup_service=tenant_lookup_service_instance,
        webhook_receiver_factory=webhook_receiver.WebhookReceiverFactory
    )



    # ============ Configure which events get published ===========
    # Not applicable for AWS EventBridge setup
    event_bus.EXTERNAL_EVENT_WHITELIST = []
    event_bus.INTERNAL_EVENT_WHITELIST = []

    # ===========Setup EventBridge event publishers ==========

    # Get configuration from environment variables
    bus_name = os.getenv("INTERNAL_EVENT_BUS_NAME")
    app_sources = os.getenv("INTERNAL_EVENT_SOURCE_NAMES").split(",")

    event_bus.internal_publisher = event_publishers.EventBridgePublisher(
        event_bus_name=bus_name,
        source_list=app_sources
    )

    # Get configuration from environment variables
    # TODO : external not yet setup in terraform
    bus_name = os.getenv("EXTERNAL_EVENT_BUS_NAME")
    app_sources = os.getenv("EXTERNAL_EVENT_SOURCE_NAMES").split(",")

    # Inject the AWS-specific publisher
    event_bus.external_publisher = event_publishers.EventBridgePublisher(
        event_bus_name=bus_name,
        source_list=app_sources
    )


    #  ================ Map event types to validation models; define to support event payloads decoder w validation ============
    event_bus.EVENT_MODELS = {}


    # =========== External async (redis/kafka/etc) event handlers (from other services) =============
    event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.update({
        "identity_gateway_service.external_events.UserLoggedInEvent": [
                lambda event: handlers.handle_user_logged_in_async_event(
                    event=event,
                ),
            ],
    })


    # ==================Internal async (redis/kafka/etc?) event handlers (within this service) ==================
    event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.update({
        "order_management.internal_events.AddOrderWebhookIntegrationEvent": [
            lambda event: handlers.handle_add_order_async_event(
                event=event,
                user_action_service=user_action_service.DynamodbUserActionService(table_name=DYNAMODB_TABLE_NAME),
                uow=repositories.DynamoOrderUnitOfWork(table_name=DYNAMODB_TABLE_NAME)
            ),
        ],
        "order_management.internal_events.ConfirmedShipmentEvent": [
            lambda event: handlers.handle_dispatch_shipment_async_event(
                event=event,
                user_action_service=user_action_service.DynamodbUserActionService(table_name=DYNAMODB_TABLE_NAME),
                shipping_provider_service=shipping.ShippingProviderService,
                uow=repositories.DynamoOrderUnitOfWork(table_name=DYNAMODB_TABLE_NAME)
            ),
        ],
        dtos.IntegrationEventType.SHIPPING_TRACKER_WEBHOOK_RECEIVED.value : [
            lambda event: handlers.handle_shipment_tracker_async_event(
                event=event,
                user_action_service=user_action_service.DynamodbUserActionService(table_name=DYNAMODB_TABLE_NAME),
                uow=repositories.DynamoOrderUnitOfWork(table_name=DYNAMODB_TABLE_NAME)
            ),
        ]
    })

    # ======================= Domain event handlers (immediate processing) ==============
    event_bus.EVENT_HANDLERS.update({
        events.CanceledOrderEvent: [
            ],
    })

    # =========== inject concrete impl / cross cutting =======================
    message_bus.ACCESS_CONTROL_SERVICE_IMPL = access_control1.AccessControlService
    #message_bus.LOGGING_SERVICE_IMPL = loggings.LoggingService
    message_bus.EXCEPTION_HANDLER_FACTORY = exception_handler.OrderExceptionHandler()
    message_bus.UOW = repositories.DynamoOrderUnitOfWork(table_name=DYNAMODB_TABLE_NAME)
    message_bus.USER_ACTION_SERVICE_IMPL = user_action_service.DynamodbUserActionService(table_name=DYNAMODB_TABLE_NAME)

    # ========= Command Handlers (write operations) ==================
    message_bus.COMMAND_HANDLERS.update({
        commands.AddOrderCommand: lambda command, **deps: handlers.handle_add_order(
            command=command,
            **deps
        ),
        commands.AddShipmentCommand: lambda command, **deps: handlers.handle_add_shipment(
            command=command,
            **deps
        ),
        commands.ConfirmShipmentCommand: lambda command, **deps: handlers.handle_confirm_shipment(
            command=command,
            #shipping_provider_service=shipping.ShippingProviderService,
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
        **handlers.webhook_publish_command_handlers.get_command_handlers(
            commands, 
            handlers, 
            event_bus,
            shipping_webhook_parser.ShippingWebhookParserResolver,
            webhook_receiver.WebhookReceiverService,
            shipment_lookup_service.DynamodbShipmentLookupService(table_name=DYNAMODB_TABLE_NAME),
            tracking_reference_extractor.TrackingReferenceExtractor
        ),
        **handlers.user_action_command_handlers.get_command_handlers(commands, handlers, application_services, tenant_lookup_service)
    })

    # ================= Query Handlers (read operations) ===================
    message_bus.QUERY_HANDLERS.update({
        queries.GetOrderQuery: lambda query, **deps: handlers.handle_get_order(
            query=query, 
            **deps
        ),
    })
