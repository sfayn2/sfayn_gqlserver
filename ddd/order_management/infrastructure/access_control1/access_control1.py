from __future__ import annotations
import requests, json
from typing import Tuple, Optional
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports, dtos

# ports.AccessControl1Abstract
class AccessControl1:
    def __init__(self, jwt_handler):
        self.jwt_handler = jwt_handler

    def get_user_context(self, token: str, request_tenant_id: str) -> dtos.UserContextDTO:
        identity_claims = self.jwt_handler.decode(token)

        # Normalize Keycloak's 'organization' claim or other iDps follow the same way w keycloak
        raw_orgs = identity_claims.get("organization", [])
        
        # Extract keys if it's a dict, otherwise treat as list
        allowed_tenants = list(raw_orgs.keys()) if isinstance(raw_orgs, dict) else list(raw_orgs)
        allowed_tenants = [str(t) for t in allowed_tenants]

        # SECURITY CHECK: Match the request to the allowed list
        if request_tenant_id not in allowed_tenants:
            #logger.error(f"Unauthorized: User {identity_claims.get('sub')} tried to access {request_tenant_id}")
            raise exceptions.AccessControlException(f"You do not have access to tenant: {request_tenant_id}")

        user_ctx = dtos.UserContextDTO.model_validate({
            "sub": identity_claims.get("sub"),
            "token_type": identity_claims.get("typ"),
            "tenant_id": request_tenant_id,  # Use the validated requested ID
            "roles": identity_claims.get("roles", []),
        })

        return user_ctx


    def ensure_user_is_authorized_for(
        self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
    ) -> bool:

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
                auth_scope = json.loads(authorization.scope)
                if all(auth_scope.get(k) == v for k, v in required_scope.items()):
                    return True

            raise exceptions.AccessControlException("Access denied: required scoped permission not found")
        elif not matching_authorizations.exists():
            raise exceptions.AccessControlException("Access denied: permission not granted")

        return True
