from __future__ import annotations
import requests
from typing import Tuple
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports

# ===============================
#TODO to have this in separate auth_service
# =====================
class AccessControlService(ports.AccessControlServiceAbstract):
    def __init__(self, jwt_handler: str, userinfo_url: str):
        self.jwt_handler = jwt_handler
        self.userinfo_url = userinfo_url

    def get_user_context(self, token: str):
        identity_claims = self.jwt_handler.decode(jwt_token)
        user_id = identity_claims["sub"]
        token_type = identity_claims.get("token_type", "Bearer")

        user_info = self._fetch_userinfo(jwt_token, token_type)
        return user_id, user_info

    def ensure_user_is_authorized_for(
        self, token: str, required_permission: str, required_scope: dict = None
    ) -> Tuple(bool, dict):

        #identity_claims = self.jwt_handler.decode(jwt_token)
        #user_id = identity_claims["sub"]
        #token_type = identity_claims.get("token_type", "Bearer")

        #user_info = self._fetch_userinfo(jwt_token, token_type)
        user_id, user_info = self.get_user_context(token)

        matching_authorizations = django_snapshopts.UserAuthorization.objects.filter(
            user_id=user_id,
            permission_codename=required_permission
        )

        if required_scope:
            for authorization in matching_authorizations:
                if all(authorization.scope.get(k) == v for k, v in required_scope.items()):
                    return True, user_info

            raise exceptions.AccessControlException("Access denied: required scoped permission not found")
        elif not matching_authorizations.exists():
            raise exceptions.AccessControlException("Access denied: permission not granted")

        return True, user_info

    def _fetch_userinfo(self, jwt_token: str, token_type: str) -> dict:
        headers = {"Authorization": f"{token_type} {jwt_token}"}
        response = requests.get(self.userinfo_url, headers=headers)
        if response.status_code != 200:
            raise exceptions.AccessControlException("Failed to fetch user info")
        return response.json()
