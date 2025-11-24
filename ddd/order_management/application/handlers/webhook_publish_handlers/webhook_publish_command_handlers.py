

def get_command_handlers(commands, handlers, event_bus, shipping_webhook_resolver, webhook_receiver_service, shipment_lookup_service):
    return {
        commands.PublishAddOrderCommand: lambda command, **deps: handlers.handle_publish_add_order(
            command=command,
            event_publisher=event_bus.internal_publisher,
            webhook_receiver_service=webhook_receiver_service,
            **deps
        ),
    }
