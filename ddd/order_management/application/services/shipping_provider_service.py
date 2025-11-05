from __future__ import annotations
from typing import Dict, Any


class ShippingProviderService:
    """
    Service responsible for coordinating shipment creation across various providers.
    """

    @classmethod
    def configure(cls, saas_service: ports.TenantServiceAbstract, 
                 shipping_provider_factory: ports.ShippingProviderAbstract):
        cls.saas_service = saas_service
        cls.shipping_provider_factory = shipping_provider_factory

    @classmethod
    def _get_provider(cls, tenant_id: str) -> ports.ShippingProviderAbstract:
        """Internal helper to retrieve the correct provider instance via the factory."""
        try:
            saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("shipping_provider", {})
            return cls.shipping_provider_factory.get_shipping_provider(saas_configs)
        except Exception as e:
            # Wrap infrastructure errors in a service-specific exception if necessary
            raise RuntimeError(f"Failed to resolve shipping provider for tenant {tenant_id}") from e

    @classmethod
    def create_shipment(cls, tenant_id: str, shipment: Shipment) -> Dict[str, Any]:
        """
        Orchestrates the creation of a shipment using the tenant's configured provider.
        """
        provider = cls._get_provider(tenant_id)

        # *** DDD/Polymorphism Improvement: ***
        # We don't check 'if provider.is_cls_delivery()'.
        # We trust that the concrete provider knows how to handle create_shipment().
        # The cls DeliveryProvider should implement create_shipment() appropriately.

        result = provider.create_shipment(shipment)
        
        # Ensure result adheres to a consistent interface/schema
        return result

