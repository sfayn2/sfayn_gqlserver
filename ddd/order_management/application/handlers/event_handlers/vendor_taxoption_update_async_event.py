from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_taxoption_update_async_event(
    event: dtos.VendorTaxOptionUpdateIntegrationEvent,
    vendor_taxoption_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external tax payment option snapshot sync
    vendor_taxoption_snapshot_repo.sync(event)

    print(f"Vendor Tax Option has been updated {event}")
