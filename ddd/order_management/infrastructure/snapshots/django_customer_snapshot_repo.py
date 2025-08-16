from __future__ import annotations
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots

class DjangoCustomerSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.CustomerDetailsSnapshot.objects.filter(tenant_id=event.tenant_id, user_id=event.sub).delete()
        django_snapshots.CustomerDetailsSnapshot.objects.create(
            customer_id=event.sub,
            user_id=event.sub,
            tenant_id=event.tenant_id,
            is_active=True
        )

