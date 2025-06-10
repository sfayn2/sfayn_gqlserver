from __future__ import annotations
from order_management import models as django_snapshots


class DjangoVendorProductSnapshotSync:
    def __init__(self, vendor_product_provider: VendorProductSnapshotAbstract):
        self.vendor_product_provider = vendor_product_provider

    def sync(self):
        django_snapshots.VendorProductSnapshot.objects.all().delete()

        products = self.vendor_product_provider.get_all_products()
        for product in products:
            django_snapshots.VendorProductSnapshot.create(**product.model_dump())