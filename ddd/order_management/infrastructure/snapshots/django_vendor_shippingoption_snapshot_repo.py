from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


class DjangoVendorShippingOptionSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorShippingOptionUpdateIntegrationEvent):
        django_snapshots.VendorShippingOptionSnapshot.objects.filter(tenant_id=event.data.tenant_id, vendor_id=event.data.vendor_id, name=event.data.name).delete()
        django_snapshots.VendorShippingOptionSnapshot.objects.create(
            **event.model_dump().get("data")
        )