from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_product_update_async_event(
    event: dtos.ProductUpdateIntegrationEvent,
    product_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external produc snapshot sync
    product_snapshot_repo.sync(event)

    print(f"Product has been updated {event}")
