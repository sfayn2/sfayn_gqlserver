from __future__ import annotations
from order_management import models as django_snapshots


class DjangoCustomerSnapshotSyncService:
    def __init__(self, customer_provider: CustomerSnapshotAbstract):
        self.customer_provider = customer_provider

    def sync(self):
        django_snapshots.CustomerDetailsSnapshot.objects.all().delete()
        django_snapshots.CustomerAddressSnapshot.objects.all().delete()

        customers = self.customer_provider.get_all_customers()
        for customer in customers:
            django_snapshots.CustomerDetailsSnapshot.objects.create(**customer.model_dump())
            customer_address = self.customer_provider.get_customer_address(customer.customer_id)
            for address in customer_address:
                django_snapshots.CustomerAddressSnapshot.objects.create(**address.model_dump())