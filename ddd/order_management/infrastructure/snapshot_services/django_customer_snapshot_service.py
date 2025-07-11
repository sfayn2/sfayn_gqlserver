from __future__ import annotations
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots

class DjangoCustomerSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    #def __init__(self, customer_provider: CustomerSnapshotAbstract):
    #    self.customer_provider = customer_provider

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.CustomerDetailsSnapshot.objects.filter(user_id=event.user_id).delete()
        django_snapshots.CustomerDetailsSnapshot.objects.create(
            customer_id=event.user_id,
            user_id=event.user_id,
            first_name=event.claims.get("given_name"),
            last_name=event.claims.get("family_name"),
            email=event.claims.get("email"),
            is_active=True
        )

        shipping_address = event.claims.get("shipping_address")
        if shipping_address:
            django_snapshots.CustomerAddressSnapshot.objects.update_or_create(
                customer_id=event.user_id,
                defaults={
                    "street": event.claims.shipping_address.get("street"),
                    "city": event.claims.shipping_address.get("city"),
                    "postal": event.claims.shipping_address.get("postal"),
                    "country": event.claims.shipping_address.get("country"),
                    "state": event.claims.shipping_address.get("state"),
                    "address_type": "shipping"
                }
            )
