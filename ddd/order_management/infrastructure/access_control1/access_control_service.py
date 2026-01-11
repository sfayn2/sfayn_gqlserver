from __future__ import annotations
from typing import Any, Optional, Type
from .jwt_token_handler import JwtTokenHandler
from ddd.order_management.application import ports

# Define custom exceptions for specific error scenarios
class AccessControlServiceError(Exception):
    """Base class for webhook processing errors."""
    pass

class ConfigurationError(AccessControlServiceError):
    pass

class AccessControlService:
    """
    A singleton-like factory service using class methods to manage global 
    dependencies and create tenant-specific AccessControl objects.
    """
    
    _saas_lookup_service: Optional[ports.LookupServiceAbstract] = None
    _access_control_library: Optional[Type[ports.AccessControl1Abstract]] = None
    _jwt_handler: Optional[Type[JwtTokenHandler]] = None

    @classmethod
    def configure(
        cls, 
        saas_lookup_service: ports.LookupServiceAbstract, 
        access_control_library: Type[ports.AccessControl1Abstract],
        jwt_handler: Type[JwtTokenHandler]
    ):
        """
        Configures the global dependencies for the service, including the JWT handler factory.
        """
        cls._saas_lookup_service = saas_lookup_service
        cls._access_control_library = access_control_library
        cls._jwt_handler = jwt_handler # Store the injected factory

    @classmethod
    def _create_jwt_handler_for_tenant(cls, tenant_id: str):
        """
        Private helper method to configure and create the JWT handler using the injected factory.
        """
        if not cls._saas_lookup_service or not cls._jwt_handler:
            raise RuntimeError("AccessControlService has not been fully configured yet.")

        #SaaS Owner should own the tenant webhook configuration?
        config_source = cls._saas_lookup_service.get_tenant_config(tenant_id)

        if not config_source.configs:
            # 2. Raise a specific custom exception instead of a generic ValueError
            raise ConfigurationError(f"No configuration found for tenant_id: {tenant_id} in SaaS lookups.")

        idp_config = config_source.configs.get("idp", {})

        if not idp_config:
            # 2. Raise a specific custom exception instead of a generic ValueError
            raise ConfigurationError(f"No IdP configuration found for tenant_id: {tenant_id} in SaaS lookups.")

        # Use the injected factory to create the handler
        return cls._jwt_handler(
            public_key=idp_config["public_key"],
            issuer=idp_config["issuer"],
            audience=idp_config["audience"],
            algorithm=idp_config["algorithm"]
        )

    @classmethod
    def create_access_control(cls, tenant_id: str) -> ports.AccessControl1Abstract:
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