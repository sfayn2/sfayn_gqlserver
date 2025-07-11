from __future__ import annotations
from typing import Dict, List
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots


class DjangoUserAuthorizationSnapshotSyncService(ports.SnapshotSyncServiceAbstract):
    def __init__(self, role_map: Dict[str, List[str]):
        self.role_map = role_map

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        django_snapshots.UserAuthorization.objects.filter(user_id=event.user_id).delete()

        for role in event.claims.realm_access.get("roles"):
            permissions = self.role_map.get(role, [])
            scope = {"tenant_id": event.claims.get("tenant_id")}

            # customer_id or vendor_id
            if role == "customer":
                scope["customer_id"] = event.user_id
            elif role == "vendor":
                scope["vendor_id"] = event.user_id
            for perm in permissions:

                django_snapshots.UserAuthorization.objects.create(
                    user_id=event.user_id,
                    permission_code_name=perm,
                    scope=scope
                )
