from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


class DjangoVendorShippingOptionSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorShippingOptionUpdateIntegrationEvent):
        django_snapshots.VendorShippingOptionSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            vendor_id=event.data.vendor_id, 
            option_name=event.data.option_name,
            defaults=event.model_dump().get("data")
        )