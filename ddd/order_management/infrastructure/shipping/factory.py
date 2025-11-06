from __future__ import annotations
from typing import Any, Optional, Dict
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

    # A dictionary mapping provider names (lowercase for consistency) to their classes
    _PROVIDER_MAP: Dict[str, Type[ports.ShippingProviderAbstract]] = {
        "easypost": EasyPostShippingProvider,
        "ninjavan": NinjaVanShippingProvider,
        "shipbob": ShipBobShippingProvider,
        "selfdelivery": SelfDeliveryProvider,
    }
    
    @staticmethod
    def get_shipping_provider(cfg: dict) -> ports.ShippingProviderAbstract:
        """
        Factory method to create the appropriate ShippingProvider instance 
        based on configuration.
        """
        provider_name = cfg.get("provider_name", "").lower()
        
        # Use dictionary lookup to find the correct class
        provider_class = ShippingProviderFactory._PROVIDER_MAP.get(provider_name)

        if provider_class:
            # Determine which configuration parameters to pass.
            # This logic needs to handle the specific needs of each provider.
            if provider_name == "selfdelivery":
                # SelfDeliveryProvider takes no arguments
                return provider_class() 
            else:
                # Other providers (Easypost, Ninjavan, Shipbob) share common arguments
                return provider_class(
                    api_key=cfg.get("api_key"),
                    endpoint=cfg.get("endpoint"),
                )
        else:
            # Raise a specific, informative exception
            raise UnknownShippingProviderError(
                f"Configuration error: Unknown shipping provider name '{provider_name}'."
            )
