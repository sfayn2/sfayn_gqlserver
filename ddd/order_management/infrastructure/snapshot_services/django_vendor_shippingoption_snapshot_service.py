from __future__ import annotations
from order_management import models as django_snapshots


class DjangoVendorShippingOptionSnapshotSyncService:
    def __init__(self, vendor_shippingoption_provider: VendorShippingOptionSnapshotAbstract):
        self.vendor_shippingoption_provider = vendor_shippingoption_provider

    def sync(self):
        django_snapshots.VendorShippingOptionSnapshot.objects.all().delete()

        vendor_shipping_options = self.vendor_shippingoption_provider.get_all_shipping_options()
        for option in vendor_shipping_options:
            django_snapshots.VendorShippingOptionSnapshot.objects.create(**option.model_dump())