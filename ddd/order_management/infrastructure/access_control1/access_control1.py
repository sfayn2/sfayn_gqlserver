from __future__ import annotations
import requests
from typing import Tuple
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports, dtos

class AccessControl1(ports.AccessControl1Abstract):
    def __init__(self, jwt_handler: str):
        self.jwt_handler = jwt_handler
        #self.userinfo_url = userinfo_url

    def ensure_user_is_authorized_for(
        self, token: str, required_permission: str, required_scope: dict = None
    ) -> dtos.UserLoggedInIntegrationEvent:

        identity_claims = self.jwt_handler.decode(token)
        token_type = identity_claims.get("token_type", "Bearer")
        #claims = self._fetch_userinfo(jwt_token, token_type)

        valid_claims = dtos.UserLoggedInIntegrationEvent.model_validate(**claims)
        #user_id = identity_claims["sub"]
        #tenant_id = identity_claims["tenant_id"]
        #roles = identity_claims.get("roles")


        matching_authorizations = django_snapshots.UserAuthorizationSnapshot.objects.filter(
            user_id=valid_claims.sub,
            tenant_id=valid_claims.tenant_id,
            permission_codename=required_permission
        )

        if required_scope:
            for authorization in matching_authorizations:
                if all(authorization.scope.get(k) == v for k, v in required_scope.items()):
                    return valid_claims

            raise exceptions.AccessControlException("Access denied: required scoped permission not found")
        elif not matching_authorizations.exists():
            raise exceptions.AccessControlException("Access denied: permission not granted")

        return valid_claims

    #def _fetch_userinfo(self, jwt_token: str, token_type: str) -> dict:
    #    headers = {"Authorization": f"{token_type} {jwt_token}"}
    #    response = requests.get(self.userinfo_url, headers=headers)
    #    if response.status_code != 200:
    #        raise exceptions.AccessControlException("Failed to fetch user info")
    #    return response.json()
