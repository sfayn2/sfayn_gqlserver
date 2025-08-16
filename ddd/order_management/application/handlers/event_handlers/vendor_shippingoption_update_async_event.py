from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_shippingoption_update_async_event(
    event: dtos.VendorShippingOptionUpdateIntegrationEvent,
    vendor_shippingoption_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external vendor shipping option snapshot sync
    vendor_shippingoption_snapshot_repo.sync(event)

    print(f"Vendor Shipping Option has been updated {event}")
