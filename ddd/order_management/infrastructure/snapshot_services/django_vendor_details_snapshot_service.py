from __future__ import annotations
from typing import Dict
from ddd.order_management.application import ports
from order_management import models as django_snapshots


class DjangoVendorDetailsSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    #def __init__(self, vendor_provider: VendorDetailsSnapshotAbstract):
    #    self.vendor_provider = vendor_provider

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.VendorDetailsSnapshot.objects.filter(vendor_id=event.claims.vendor_id).delete()
        django_snapshots.VendorDetailsSnapshot.objects.create(
            vendor_id=event.claims.vendor_id,
            vendor_name=event.claims.vendor_name,
            vendor_country=event.claims.vendor_country,
            tenant_id=event.tenant_id,
            is_active=True
        )