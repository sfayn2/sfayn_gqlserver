from __future__ import annotations

class AccessControlService:

    @classmethod
    def configure(cls, saas_service, access_control1):
        cls.saas_service = saas_service
        cls.access_control1 = access_control1

    @classmethod
    def _get_jwt_handler_for_tenant(cls, tenant_id: str):
        sass_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("idp", {})
        
        return cls.access_control1.JwtTokenHandler(
            public_key=saas_configs.get("public_key"),
            issuer=saas_configs.get("issuer"),
            audience=saas_configs.get("audience"),
            algorithm=saas_configs.get("algorithm")
        )

    @classmethod
    def resolve(cls, tenant_id: str):

        access_control = cls.access_control1.AccessControl1(
            jwt_handler=cls._get_jwt_handler_for_tenant(tenant_id)
        )

        return access_control
