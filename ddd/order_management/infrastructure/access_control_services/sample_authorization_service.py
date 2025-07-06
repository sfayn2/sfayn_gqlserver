from __future__ import annotations
import uuid
from ddd.order_management.application import ports
from order_management import models as django_snapshots

class SampleAuthorizationService(ports.AuthorizationServiceAbstract):
    def can(self, user_id: uuid.UUID, permission: str, scope: dict = None) -> bool:
        perms = django_snapshots.UserAuthorizationSnapshot.objects.filter(
            user_id=user_id,
            permission_codename=permission
        )

        if not scope:
            return perms.exists()

        for perm in perms:
            if all(perm.scope.get(k) == v for k, v in scope.items()):
                return True

        return False
