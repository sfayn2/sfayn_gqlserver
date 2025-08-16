from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_details_update_async_event(
    event: dtos.VendorDetailsUpdateIntegrationEvent,
    vendor_details_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external produc snapshot sync
    vendor_details_snapshot_repo.sync(event)

    print(f"Vendor Details has been updated {event}")
