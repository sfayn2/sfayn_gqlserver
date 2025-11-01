from __future__ import annotations
from typing import Any
from datetime import datetime
from .self_delivery_provider import SelfDeliveryProvider
from .easypost_provider import EasyPostShippingProvider
from .ninjavan_provider import NinjaVanShippingProvider
from .shipbob_provider import ShipBobShippingProvider
from .enums import ShippingProviderEnum


class ShippingProviderResolver:
    @staticmethod
    def resolve(config: dict):
        provider_cfg = config.get("shipping_provider")
        provider_type = provider_cfg.get("type")
        if provider_type == ShippingProviderEnum.EASYPOST.value:
            return EasyPostShippingProvider(
                api_key=provider_cfg.get("api_key"),
                endpoint=provider_cfg.get("endpoint"),
            )
        elif provider_type == ShippingProviderEnum.NINJAVAN.value:
            return NinjaVanShippingProvider(
                api_key=provider_cfg.get("api_key"),
                endpoint=provider_cfg.get("endpoint"),
            )
        elif provider_type == ShippingProviderEnum.SHIPBOB.value:
            return ShipBobShippingProvider(
                api_key=provider_cfg.get("api_key"),
                endpoint=provider_cfg.get("endpoint"),
            )
        elif provider_type == ShippingProviderEnum.SELFDELIVERY.value:
            return SelfDeliveryProvider()
