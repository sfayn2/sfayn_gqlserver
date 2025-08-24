from __future__ import annotations
from typing import Dict
from ddd.order_management.application import ports
from order_management import models as django_snapshots


class DjangoVendorDetailsSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorDetailsUpdateIntegrationEvent):
        django_snapshots.VendorDetailsSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            vendor_id=event.data.vendor_id,
            defaults=event.model_dump().get("data")
        )