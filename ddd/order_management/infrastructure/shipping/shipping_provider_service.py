from __future__ import annotations
from typing import Dict, Any, Optional
from .shipping_provider_abstract import ShippingProviderAbstract
from .factory import ShippingProviderFactory
from ddd.order_management.application import (
    ports,
    dtos
)
from ddd.order_management.domain import models

# ports.ShippingProviderServiceAbstract
class ShippingProviderService:
    """
    Service responsible for coordinating shipment creation across various providers.
    """
    saas_lookup_service: Optional[ports.LookupServiceAbstract] = None
    shipping_provider_factory: Optional[ShippingProviderFactory] = None

    @classmethod
    def configure(cls, saas_lookup_service: ports.LookupServiceAbstract, 
                 shipping_provider_factory: ShippingProviderFactory):
        cls.saas_lookup_service = saas_lookup_service
        cls.shipping_provider_factory = shipping_provider_factory

    @classmethod
    def _get_provider(cls, tenant_id: str) -> ShippingProviderAbstract:
        """Internal helper to retrieve the correct provider instance via the factory."""
        
        if cls.saas_lookup_service is None:
            raise RuntimeError("ShippingProviderService has not been configured yet (missing saas_lookup_service).")

        if cls.shipping_provider_factory is None:
            raise RuntimeError("ShippingProviderService has not been configured yet (missing shipping_provider_factory).")

            
        try:
            saas_configs = cls.saas_lookup_service.get_tenant_config(tenant_id).configs.get("shipping_provider", {})
            return cls.shipping_provider_factory.get_shipping_provider(saas_configs)
        except Exception as e:
            # Handle potential exceptions during config retrieval
            raise RuntimeError(f"Failed to retrieve shipping config for tenant {tenant_id}: {e}")


    @classmethod
    def create_shipment(cls, tenant_id: str, shipment: models.Shipment) -> dtos.CreateShipmentResponseDTO:
        """
        Orchestrates the creation of a shipment using the tenant's configured provider.
        """
        provider = cls._get_provider(tenant_id)

        # *** DDD/Polymorphism Improvement: ***
        # We don't check 'if provider.is_cls_delivery()'.
        # We trust that the concrete provider knows how to handle create_shipment().
        # The cls DeliveryProvider should implement create_shipment() appropriately.

        result = provider.create_shipment(shipment, tenant_id)
        
        # Ensure result adheres to a consistent interface/schema
        return result

