from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_product_update_async_event(
    event: dtos.ProductUpdateIntegrationEvent,
    product_sync: ports.SnapshotSyncServiceAbstract
):

    # sync external produc snapshot sync
    product_sync.sync(event)

    print(f"Product has been updated {event}")
