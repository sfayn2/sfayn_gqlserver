from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos,
    shared
)
from ddd.order_management.domain import events, exceptions

def handle_publish_tenant_workflow_update(
    command: commands.PublishTenantWorkflowUpdateCommand, 
    event_publisher: ports.EventPublisherAbstract
):
    try:
        event = dtos.TenantWorkflowUpdateIntegrationEvent(
            **command.model_dump()
        )

        event_publisher.publish(event)

        return dtos.ResponseDTO(
            success=True,
            message="Tenant Workflow update has been published."
        )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


