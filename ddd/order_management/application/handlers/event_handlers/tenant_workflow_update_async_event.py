from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_tenant_workflow_update_async_event(
    event: dtos.TenantWorkflowUpdateIntegrationEvent,
    tenant_workflow_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external produc snapshot sync
    tenant_workflow_snapshot_repo.sync(event)

    print(f"Tenant workflow has been updated {event}")
