from __future__ import annotations
from typing import Dict, List
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots


class DjangoUserAuthorizationSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    def __init__(self, role_map: Dict[str, List[str]]):
        self.role_map = role_map

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.UserAuthorizationSnapshot.objects.filter(user_id=event.sub).delete()

        for role in event.claims.roles:
            permissions = self.role_map.get(role, [])
            scope = {}

            # customer_id or vendor_id
            if role == "customer":
                scope["customer_id"] = event.sub
            elif role == "vendor":
                scope["vendor_id"] = event.sub
            for perm in permissions:

                django_snapshots.UserAuthorizationSnapshot.objects.create(
                    user_id=event.sub,
                    tenant_id=event.tenant_id,
                    permission_codename=perm,
                    scope=scope
                )
