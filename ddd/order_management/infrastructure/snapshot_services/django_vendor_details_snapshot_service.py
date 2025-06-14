from __future__ import annotations
from order_management import models as django_snapshots


class DjangoVendorDetailsSnapshotSyncService:
    def __init__(self, vendor_provider: VendorDetailsSnapshotAbstract):
        self.vendor_provider = vendor_provider

    def sync(self):
        django_snapshots.VendorDetailsSnapshot.objects.all().delete()

        vendors = self.vendor_provider.get_all_vendors()
        for vendor in vendors:
            django_snapshots.VendorDetailsSnapshot.objects.create(**vendor.model_dump())