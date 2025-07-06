from __future__ import annotations
from typing import Tuple
from order_management import models as django_snapshots
#from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports

class AccessControlService(ports.AccessControlServiceAbstract):
    def __init__(self, jwt_handler):
        self.jwt_handler = jwt_handler

    def ensure_user_has(self, token: str, permission: str, scope: dict = None) -> Tuple(bool, dict):

        decoded = self.jwt_handler.decode(token)
        user_id = decoded["sub"]

        qs = django_snapshopts.UserAuthorization.objects.filter(
            user_id=user_id,
            permission_codename=permission
        )

        if scope:
            for qry in qs:
                if all(qry.scope.get(k) == v for k, v in scope.items()):
                    return True, decoded

            raise Exception("Permission denied")
        elif not qs.exists():
            raise Exception("Permission denied")

        return True, decoded
