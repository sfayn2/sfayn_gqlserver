from __future__ import annotations
from typing import Dict, List
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots


class DjangoUserAuthorizationSnapshotRepo(ports.SnapshotRepoAbstract):
    #def __init__(self, role_map: Dict[str, List[str]]):
    #    self.role_map = role_map

    def sync(self, event: dtos.UserLoggedInIntegrationEvent):

        for role in event.roles:
            #permissions = self.role_map.get(role, [])
            permissions = django_snapshots.TenantRolePermissionSnapshot.objects.filter(
                tenant_id=event.tenant_id, 
                role=role, 
                is_active=True
            ).values_list("permission_codename", flat=True)

            scope = {}

            # customer_id or vendor_id
            if role == "customer":
                scope["customer_id"] = event.sub
            elif role == "vendor":
                scope["vendor_id"] = event.sub
            for perm in permissions:

                django_snapshots.UserAuthorizationSnapshot.objects.update_or_create(
                    user_id=event.sub,
                    tenant_id=event.tenant_id,
                    defaults={
                        "permission_codename": perm,
                        "scope":scope
                    }
                )
