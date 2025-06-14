from django.core.management.base  import BaseCommand
from ddd.order_management.infrastructure import bootstrap_snapshots

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bootstrap_snapshots.run_customer_snapshot_sync()

        self.stdout.write("Customer snapshot synced.")