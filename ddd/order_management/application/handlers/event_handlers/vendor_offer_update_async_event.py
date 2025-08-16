from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_offer_update_async_event(
    event: dtos.VendorOfferUpdateIntegrationEvent,
    vendor_offer_snapshot_repo: ports.SnapshotRepoAbstract
):

    # sync external vendor offer snapshot sync
    vendor_offer_snapshot_repo.sync(event)

    print(f"Vendor Offer has been updated {event}")
