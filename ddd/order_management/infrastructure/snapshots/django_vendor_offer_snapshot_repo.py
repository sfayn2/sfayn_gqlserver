from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports

class DjangoVendorOfferSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorOfferUpdateIntegrationEvent):
        django_snapshots.VendorOfferSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            vendor_id=event.data.vendor_id, 
            offer_id=event.data.offer_id,
            defaults=event.model_dump().get("data")
        )

