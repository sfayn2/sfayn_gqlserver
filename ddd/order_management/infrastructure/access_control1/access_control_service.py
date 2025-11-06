from __future__ import annotations
from typing import Any, Optional

class AccessControlService:
    """
    A singleton-like factory service using class methods to manage global 
    dependencies and create tenant-specific AccessControl objects.
    """
    
    #_saas_service: Optional[SaasServiceLike] = None
    #_access_control_library_class: Optional[Type[AccessControl1Like]] = None
    ## Injected factory function that creates the JwtTokenHandler
    #_jwt_handler: Optional[JwtHandlerFactory] = None

    @classmethod
    def configure(
        cls, 
        saas_service, 
        access_control_library,
        jwt_handler
    ):
        """
        Configures the global dependencies for the service, including the JWT handler factory.
        """
        cls._saas_service = saas_service
        cls._access_control_library = access_control_library
        cls._jwt_handler = jwt_handler # Store the injected factory

    @classmethod
    def _create_jwt_handler_for_tenant(cls, tenant_id: str):
        """
        Private helper method to configure and create the JWT handler using the injected factory.
        """
        if not cls._saas_service or not cls._jwt_handler:
            raise RuntimeError("AccessControlService has not been fully configured yet.")

        tenant_config = cls._saas_service.get_tenant_config(tenant_id)
        saas_configs = tenant_config.configs.get("idp", {})
        
        # Use the injected factory to create the handler
        return cls._jwt_handler(
            public_key=saas_configs.get("public_key"),
            issuer=saas_configs.get("issuer"),
            audience=saas_configs.get("audience"),
            algorithm=saas_configs.get("algorithm")
        )

    @classmethod
    def create_access_control(cls, tenant_id: str):
        """
        Factory method: Creates and returns a fully configured AccessControl 
        instance tailored for the given tenant ID.
        """
        if not cls._access_control_library:
            raise RuntimeError("AccessControlService has not been fully configured yet.")
            
        jwt_handler = cls._create_jwt_handler_for_tenant(tenant_id)

        # The access control object is constructed here
        access_control = cls._access_control_library(
            jwt_handler=jwt_handler
        )

        return access_control