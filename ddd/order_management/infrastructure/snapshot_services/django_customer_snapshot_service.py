from __future__ import annotations
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots

class DjangoCustomerSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    #def __init__(self, customer_provider: CustomerSnapshotAbstract):
    #    self.customer_provider = customer_provider

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.CustomerDetailsSnapshot.objects.filter(user_id=event.sub).delete()
        django_snapshots.CustomerDetailsSnapshot.objects.create(
            customer_id=event.sub,
            user_id=event.sub,
            first_name=event.claims.given_name,
            last_name=event.claims.family_name,
            email=event.claims.email,
            tenant_id=event.tenant_id,
            is_active=True
        )

        shipping_address = event.claims.shipping_address
        if shipping_address:
            django_snapshots.CustomerAddressSnapshot.objects.update_or_create(
                customer_id=event.sub,
                defaults={
                    "street": event.claims.shipping_address.street,
                    "city": event.claims.shipping_address.city,
                    "postal": event.claims.shipping_address.postal,
                    "country": event.claims.shipping_address.country,
                    "state": event.claims.shipping_address.state,
                    "address_type": "shipping"
                }
            )
