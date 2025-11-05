from __future__ import annotations
from typing import Any, Optional
from datetime import datetime
from .self_delivery_provider import SelfDeliveryProvider
from .easypost_provider import EasyPostShippingProvider
from .ninjavan_provider import NinjaVanShippingProvider
from .shipbob_provider import ShipBobShippingProvider


# Define a custom exception for better error clarity
class UnknownShippingProviderError(Exception):
    """Raised when the requested shipping provider name is unknown."""
    pass


class ShippingProviderFactory:
    
    @staticmethod
    def get_shipping_provider(cfg: dict) -> ports.ShippingProviderAbstract:
        """
        Factory method to create the appropriate ShippingProvider instance 
        based on configuration.
        """
        provider_name = cfg.get("provider_name", "").upper()
        
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
        else:
            # Raise a specific, informative exception
            raise UnknownShippingProviderError(
                f"Configuration error: Unknown shipping provider name '{provider_name}'."
            )

