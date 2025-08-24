from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


class DjangoVendorProductSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.ProductUpdateIntegrationEvent):
        django_snapshots.VendorProductSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            product_id=event.data.product_id,
            defaults=event.model_dump().get("data")
        )