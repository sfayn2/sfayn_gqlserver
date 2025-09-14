from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_tenant_rolemap_async_event(
    event: dtos.TenantRolemapUpdateIntegrationEvent,
    tenant_rolemap_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external produc snapshot sync
    tenant_rolemap_snapshot_repo.sync(event)

    print(f"Tenant Rolemap has been updated {event}")
