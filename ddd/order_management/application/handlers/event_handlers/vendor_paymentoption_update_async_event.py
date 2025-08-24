from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_paymentoption_update_async_event(
    event: dtos.VendorPaymentOptionUpdateIntegrationEvent,
    vendor_paymentoption_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external vendor payment option snapshot sync
    vendor_paymentoption_snapshot_repo.sync(event)

    print(f"Vendor Payment Option has been updated {event}")
