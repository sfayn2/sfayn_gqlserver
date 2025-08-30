from __future__ import annotations
import requests
from typing import Tuple, Optional
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports, dtos

class AccessControl1(ports.AccessControl1Abstract):
    def __init__(self, jwt_handler):
        self.jwt_handler = jwt_handler
        #self.userinfo_url = userinfo_url

    def ensure_user_is_authorized_for(
        self, token: str, required_permission: str, required_scope: Optional[dict] = None
    ) -> dtos.Identity:

        identity_claims = self.jwt_handler.decode(token)
        token_type = identity_claims.get("token_type", "Bearer")

        valid_claims = dtos.Identity.model_validate(identity_claims)

        #TODO: this should not be here? lets inject 
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
