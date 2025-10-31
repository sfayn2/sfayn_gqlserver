from __future__ import annotations
from .fedex_provider import FedExShippingProvider
from .self_delivery_provider import SelfDeliveryProvider
from .easypost_provider import EasyPostShippingProvider

class ShippingProviderResolver:
    @staticmethod
    def resolve(config: dict):
        provider_cfg = config.get("shipping_provider")
        provider_type = provider_cfg.get("type")
        if provider_type == "FedEx":
            return FedExShippingProvider(
                api_key=provider_cfg.get("api_key"),
                account_number=provider_cfg.get("account_number"),
                endpoint=provider_cfg.get("endpoint"),
            )
        elif provider_type == "EasyPost":
            return EasyPostShippingProvider(
                api_key=provider_cfg.get("api_key"),
                endpoint=provider_cfg.get("endpoint"),
            )
        elif provider_type == "SelfDelivery":
            return SelfDeliveryProvider()
