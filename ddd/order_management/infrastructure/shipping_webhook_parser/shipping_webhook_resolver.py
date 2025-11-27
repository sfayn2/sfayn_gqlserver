from __future__ import annotations
from typing import Dict, Any, Optional
from .shipping_webhook_parser_abstract import ShippingWebhookParserAbstract
from .shipping_webhook_parser_factory import ShippingWebhookParserFactory
from ddd.order_management.application import (
    ports,
    dtos,
    mappers
)
from ddd.order_management.domain import models

# Define custom exceptions for specific error scenarios
class ConfigurationError(Exception):
    pass

# ports.ShippingWebhookResolverAbstract
class ShippingWebhookResolver:
    """
    Service responsible for coordinating shipment creation across various parsers.
    """
    saas_lookup_service: Optional[ports.LookupServiceAbstract] = None
    tenant_lookup_service: Optional[ports.LookupServiceAbstract] = None
    shipping_parser_factory: Optional[ShippingWebhookParserFactory] = None

    @classmethod
    def configure(cls, saas_lookup_service: ports.LookupServiceAbstract, 
                  tenant_lookup_service: ports.LookupServiceAbstract,
                 shipping_parser_factory: ShippingWebhookParserFactory):
        cls.saas_lookup_service = saas_lookup_service
        cls.tenant_lookup_service = tenant_lookup_service
        cls.shipping_parser_factory = shipping_parser_factory

    @classmethod
    def _get_parser(cls, tenant_id: str) -> ShippingWebhookParserAbstract:
        """Internal helper to retrieve the correct parser instance via the factory."""
        
        if cls.saas_lookup_service is None:
            raise RuntimeError("ShippingparserService has not been configured yet (missing saas_lookup_service).")

        if cls.tenant_lookup_service is None:
            raise RuntimeError("ShippingparserService has not been configured yet (missing tenant_lookup_service).")

        if cls.shipping_parser_factory is None:
            raise RuntimeError("ShippingparserService has not been configured yet (missing shipping_parser_factory).")

        try:
            # Lets Saas Owner handl webhook related configs 
            ## 1. Type Hinting & Clearer Variable Names
            #tenant_source = cls.tenant_lookup_service.get_tenant_config(tenant_id)
            #saas_source = cls.saas_lookup_service.get_tenant_config(tenant_id)
            
            ## Determine the primary source of configuration data
            #config_source = tenant_source.configs if tenant_source and tenant_source.configs else saas_source.configs

            config_source = cls.saas_lookup_service.get_tenant_config(tenant_id)

            if not config_source:
                # 2. Raise a specific custom exception instead of a generic ValueError
                raise ConfigurationError(f"No configuration found for tenant_id: {tenant_id} in both tenant and SaaS lookups.")

            # 3. Defensive coding: Ensure field names are consistent
            # Corrected DTO field name 'shipment_webhook_max_age_seconds' used consistently
            shipment_config = mappers.ConfigMapper.to_shipment_config_dto(config_source)
        
            return cls.shipping_parser_factory.get_payload_parser(shipment_config)

        except Exception as e:
            raise ConfigurationError("Error getting shipment provider")


            
        #try:
        #    saas_configs = cls.saas_lookup_service.get_tenant_config(tenant_id).configs.get("shipping_webhook", {})
        #    return cls.shipping_parser_factory.get_payload_parser(saas_configs)
        #except Exception as e:
        #    # Handle potential exceptions during config retrieval
        #    raise RuntimeError(f"Failed to retrieve shipping config for tenant {tenant_id}: {e}")

    @classmethod
    def resolve(cls, tenant_id: str, payload: Any) -> dtos.ShippingWebhookDTO:
        """
        Orchestrates the creation of a shipment using the tenant's configured parser.
        """
        parser = cls._get_parser(tenant_id)

        result = parser.parse(payload)
        
        # Ensure result adheres to a consistent interface/schema
        return result

