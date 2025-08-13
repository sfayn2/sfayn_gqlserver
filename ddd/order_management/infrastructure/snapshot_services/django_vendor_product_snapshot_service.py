from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


#class DjangoVendorProductSnapshotSyncService:
class DjangoVendorProductSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    #def __init__(self, vendor_product_provider: VendorProductSnapshotAbstract):
    #    self.vendor_product_provider = vendor_product_provider

    def sync(self, event: dtos.ProductUpdateIntegrationEvent):
        django_snapshots.VendorProductSnapshot.objects.filter(tenant_id=event.data.tenant_id, product_id=event.data.product_id).delete()
        django_snapshots.VendorProductSnapshot.objects.create(
            **event.model_dump().get("data")
        )
        #django_snapshots.VendorProductSnapshot.objects.all().delete()

        #products = self.vendor_product_provider.get_all_products()
        #for product in products:
        #    django_snapshots.VendorProductSnapshot.objects.create(**product.model_dump())