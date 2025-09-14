

def get_command_handlers(commands, handlers, event_bus):
    return {
        commands.PublishTenantWorkflowUpdateCommand: lambda command, **deps: handlers.handle_publish_tenant_workflow_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishTenantRolemapUpdateCommand: lambda command, **deps: handlers.handle_publish_tenant_rolemap_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishTenantCreateOrderCommand: lambda command, **deps: handlers.handle_publish_tenant_create_order(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
    }
