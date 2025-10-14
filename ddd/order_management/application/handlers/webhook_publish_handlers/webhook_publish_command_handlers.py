

def get_command_handlers(commands, handlers, event_bus):
    return {
        commands.PublishCreateOrderCommand: lambda command, **deps: handlers.handle_publish_tenant_create_order(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
    }
