from django.core.management.base  import BaseCommand
from ddd.order_management.infrastructure import bootstrap_snapshots

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bootstrap_snapshots.run_vendor_offer_snapshot_sync()

        self.stdout.write("Vendor Offer snapshot synced.")