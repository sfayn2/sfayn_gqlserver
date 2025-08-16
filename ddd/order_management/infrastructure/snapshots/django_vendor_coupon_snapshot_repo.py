from __future__ import annotations
from typing import Dict
from ddd.order_management.application import ports
from order_management import models as django_snapshots


class DjangoVendorCouponSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorCouponUpdateIntegrationEvent):
        django_snapshots.VendorCouponSnapshot.objects.filter(tenant_id=event.data.tenant_id, vendor_id=event.data.vendor_id, coupon_code=event.data.coupon_code).delete()
        django_snapshots.VendorCouponSnapshot.objects.create(
            **event.model_dump().get("data")
        )