from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports


class DjangoVendorTaxOptionSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.VendorTaxOptionUpdateIntegrationEvent):
        django_snapshots.VendorTaxOptionSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            vendor_id=event.data.vendor_id, 
            tax_type=event.data.tax_type,
            provider=event.data.provider,
            defaults=event.model_dump().get("data")
        )