from django.core.management.base  import BaseCommand
from ddd.order_management.infrastructure import snapshots_sync, adapters

class VendorOfferSnapshotSyncCommand(BaseCommand):
    def handle(self, *args, **kwargs):
        provider = adapters.FakeVendorOfferAdapter()
        django_vendor_offer_snapshot = snapshots_sync.DjangoVendorOfferSnapshotSync(provider)
        django_vendor_offer_snapshot.sync()

        self.stdout.write("Vendor Offer snapshot synced.")