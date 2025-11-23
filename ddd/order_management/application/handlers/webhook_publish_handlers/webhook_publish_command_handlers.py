

def get_command_handlers(commands, handlers, event_bus, shipping_webhook_resolver, webhook_receiver_service):
    return {
        commands.PublishAddOrderCommand: lambda command, **deps: handlers.handle_publish_add_order(
            command=command,
            event_publisher=event_bus.internal_publisher,
            shipping_webhook_resolver=shipping_webhook_resolver,
            webhook_receiver_service=webhook_receiver_service,
            **deps
        ),
    }
