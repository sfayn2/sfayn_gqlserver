from __future__ import annotations
from typing import Any
from datetime import datetime
from .self_delivery_provider import SelfDeliveryProvider
from .easypost_provider import EasyPostShippingProvider
from .ninjavan_provider import NinjaVanShippingProvider
from .shipbob_provider import ShipBobShippingProvider


class ShippingProviderResolver:
    @staticmethod
    def resolve(config: dict):
        shipping_cfg = config.get("shipping")
        provider_type = shipping_cfg.get("provider")
        if provider_type == "EASYPOST":
            return EasyPostShippingProvider(
                api_key=shipping_cfg.get("api_key"),
                endpoint=shipping_cfg.get("endpoint"),
            )
        elif provider_type == "NINJAVAN":
            return NinjaVanShippingProvider(
                api_key=shipping_cfg.get("api_key"),
                endpoint=shipping_cfg.get("endpoint"),
            )
        elif provider_type == "SHIPBOB":
            return ShipBobShippingProvider(
                api_key=shipping_cfg.get("api_key"),
                endpoint=shipping_cfg.get("endpoint"),
            )
        elif provider_type == "SELFDELIVERY":
            return SelfDeliveryProvider()
