from __future__ import annotations
from typing import Dict
from ddd.order_management.application import ports
from order_management import models as django_snapshots


class DjangoVendorDetailsSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    #def __init__(self, vendor_provider: VendorDetailsSnapshotAbstract):
    #    self.vendor_provider = vendor_provider

    def sync(self, event: dtos.VendorDetailsUpdateIntegrationEvent):
        django_snapshots.VendorDetailsSnapshot.objects.filter(tenant_id=event.data.tenant_id, vendor_id=event.data.vendor_id).delete()
        django_snapshots.VendorDetailsSnapshot.objects.create(
            **event.model_dump().get("data")
        )