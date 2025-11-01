
class ShippingProviderService:

    @classmethod
    def configure(cls, saas_service, shipping_provider_resolver):
        cls.saas_service = saas_service
        cls.shipping_provider_resolver = shipping_provider_resolver

    @classmethod
    def _get_provider(cls, tenant_id: str):
        saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("shipping_provider", {})
        return cls.shipping_provider_resolver.resolve(saas_configs)

    @classmethod
    def create_shipment(cls, tenant_id: str, shipment):
        provider = self._get_provider(tenant_id)

        if provider.is_self_delivery():
            return {
                "tracking_number": f"SELF-{shipment.shipment_id[:8]}",
                "total_amount": "0.00",
                "label_url": None
            }
        else:
            result = provider.create_shipment(shipment)
            return result

