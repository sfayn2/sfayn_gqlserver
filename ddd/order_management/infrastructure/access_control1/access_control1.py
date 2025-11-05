from __future__ import annotations
import requests
from typing import Tuple, Optional
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports, dtos

# AccessControl1Abstract
class AccessControl1:
    def __init__(self, jwt_handler):
        self.jwt_handler = jwt_handler

    def get_user_context(self, token: str, request_tenant_id: str) -> dtos.UserContextDTO:
        identity_claims = self.jwt_handler.decode(token)
        token_type = identity_claims.get("token_type", "Bearer")
        user_ctx = dtos.UserContextDTO.model_validate(identity_claims)

        # verify tenant_id
        if user_ctx.tenant_id != request_tenant_id:
            raise exceptions.AccessControlException(f"Tenant mismatch token={user_ctx.tenant_id}, request={request_tenant_id}")

        return user_ctx


    def ensure_user_is_authorized_for(
        self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
    ) -> dtos.UserContextDTO:

        #identity_claims = self.jwt_handler.decode(token)
        #token_type = identity_claims.get("token_type", "Bearer")

        #valid_claims = dtos.UserContextDTO.model_validate(identity_claims)

        #TODO: this should not be here? lets inject 
        matching_authorizations = django_snapshots.UserAuthorizationSnapshot.objects.filter(
            tenant_id=user_context.tenant_id,
            permission_codename=required_permission
        )

        if required_scope:
            for authorization in matching_authorizations:
                if all(authorization.scope.get(k) == v for k, v in required_scope.items()):
                    return True

            raise exceptions.AccessControlException("Access denied: required scoped permission not found")
        elif not matching_authorizations.exists():
            raise exceptions.AccessControlException("Access denied: permission not granted")

        return True
