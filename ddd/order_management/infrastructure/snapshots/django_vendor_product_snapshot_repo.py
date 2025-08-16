from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


class DjangoVendorProductSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.ProductUpdateIntegrationEvent):
        django_snapshots.VendorProductSnapshot.objects.filter(tenant_id=event.data.tenant_id, product_id=event.data.product_id).delete()
        django_snapshots.VendorProductSnapshot.objects.create(
            **event.model_dump().get("data")
        )