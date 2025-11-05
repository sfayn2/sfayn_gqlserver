from __future__ import annotations
from typing import Any
from datetime import datetime
from .self_delivery_provider import SelfDeliveryProvider
from .easypost_provider import EasyPostShippingProvider
from .ninjavan_provider import NinjaVanShippingProvider
from .shipbob_provider import ShipBobShippingProvider


class ShippingProviderResolver:
    @staticmethod
    def resolve(cfg: dict):
        provider_name = cfg.get("provider_name")
        if provider_name == "EASYPOST":
            return EasyPostShippingProvider(
                api_key=cfg.get("api_key"),
                endpoint=cfg.get("endpoint"),
            )
        elif provider_name == "NINJAVAN":
            return NinjaVanShippingProvider(
                api_key=cfg.get("api_key"),
                endpoint=cfg.get("endpoint"),
            )
        elif provider_name == "SHIPBOB":
            return ShipBobShippingProvider(
                api_key=cfg.get("api_key"),
                endpoint=cfg.get("endpoint"),
            )
        elif provider_name == "SELFDELIVERY":
            return SelfDeliveryProvider()
