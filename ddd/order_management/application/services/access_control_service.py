from __future__ import annotations

class AccessControlService:

    def __init__(self, saas_service, access_control1):
        self.saas_service = saas_service
        self.access_control1 = access_control1

    def _get_jwt_handler_for_tenant(self, tenant_id: str):
        sass_configs = self.saas_service.get_tenant_config(tenant_id).configs.get("idp", {})
        
        return self.access_control1.JwtTokenHandler(
            public_key=saas_configs.get("public_key"),
            issuer=saas_configs.get("issuer"),
            audience=saas_configs.get("audience"),
            algorithm=saas_configs.get("algorithm")
        )

    def resolve(self, tenant_id: str):

        access_control = self.access_control1.AccessControl1(
            jwt_handler=self._get_jwt_handler_for_tenant(tenant_id)
        )

        return access_control
