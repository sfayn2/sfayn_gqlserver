from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_create_order_async_event(
    event: dtos.TenantCreateOrderIntegrationEvent,
):

    # sync external produc snapshot sync
    tenant_create_order_snapshot_repo.sync(event)

    print(f"Tenant created order {event}")
