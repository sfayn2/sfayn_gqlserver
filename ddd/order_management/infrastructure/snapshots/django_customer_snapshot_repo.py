from __future__ import annotations
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots

class DjangoCustomerSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.CustomerDetailsSnapshot.objects.update_or_create(
            tenant_id=event.tenant_id,
            user_id=event.sub,
            defaults={
                "customer_id": event.sub,
                "is_active": True
            }
        )

