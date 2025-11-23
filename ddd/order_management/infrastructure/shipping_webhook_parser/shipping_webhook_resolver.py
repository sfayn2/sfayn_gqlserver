from __future__ import annotations
from typing import Dict, Any, Optional
from .shipping_webhook_parser_abstract import ShippingWebhookParserAbstract
from .shipping_webhook_parser_factory import ShippingWebhookParserFactory
from ddd.order_management.application import (
    ports,
    dtos
)
from ddd.order_management.domain import models

# ports.ShippingWebhookResolverAbstract
class ShippingWebhookResolver:
    """
    Service responsible for coordinating shipment creation across various parsers.
    """
    saas_service: Optional[ports.TenantServiceAbstract] = None
    shipping_parser_factory: Optional[ShippingWebhookParserFactory] = None

    @classmethod
    def configure(cls, saas_service: ports.TenantServiceAbstract, 
                 shipping_parser_factory: ShippingWebhookParserFactory):
        cls.saas_service = saas_service
        cls.shipping_parser_factory = shipping_parser_factory

    @classmethod
    def _get_parser(cls, tenant_id: str) -> ShippingWebhookParserAbstract:
        """Internal helper to retrieve the correct parser instance via the factory."""
        
        if cls.saas_service is None:
            raise RuntimeError("ShippingparserService has not been configured yet (missing saas_service).")

        if cls.shipping_parser_factory is None:
            raise RuntimeError("ShippingparserService has not been configured yet (missing shipping_parser_factory).")

            
        try:
            saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("shipping_webhook", {})
            return cls.shipping_parser_factory.get_shipping_parser(saas_configs)
        except Exception as e:
            # Handle potential exceptions during config retrieval
            raise RuntimeError(f"Failed to retrieve shipping config for tenant {tenant_id}: {e}")

    @classmethod
    def resolve(cls, tenant_id: str, payload, headers) -> dtos.ShippingWebhookIntegrationEvent:
        """
        Orchestrates the creation of a shipment using the tenant's configured parser.
        """
        parser = cls._get_parser(tenant_id)

        result = parser.parse(payload, headers)
        
        # Ensure result adheres to a consistent interface/schema
        return result

