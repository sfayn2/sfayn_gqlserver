from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_vendor_coupon_update_async_event(
    event: dtos.VendorCouponUpdateIntegrationEvent,
    vendor_coupon_sync: ports.SnapshotSyncServiceAbstract
):

    # sync external vendor coupon snapshot sync
    vendor_coupon_sync.sync(event)

    print(f"Vendor Coupon has been updated {event}")
