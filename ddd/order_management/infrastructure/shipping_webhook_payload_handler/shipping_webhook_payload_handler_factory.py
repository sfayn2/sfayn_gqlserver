from __future__ import annotations
from typing import Any, Optional, Dict, Type
from datetime import datetime
from .shipping_webhook_payload_handler_abstract import ShippingWebhookPayloadHandlerAbstract
from .easypost_shipping_webhook_payload_handler import EasyPostShippingWebhookPayloadHandler


# Define a custom exception for better error clarity
class UnknownShippingProviderError(Exception):
    """Raised when the requested shipping provider name is unknown."""
    pass


class ShippingWebhookPayloadHandlerFactory:

    # A dictionary mapping provider names (lowercase for consistency) to their classes
    _HANDLER_MAP: Dict[str, Type[ShippingWebhookPayloadHandlerAbstract]] = {
        "easypost": EasyPostShippingWebhookPayloadHandler,
    }
    
    @staticmethod
    def get_payload_handler(cfg: dict) -> ShippingWebhookPayloadHandlerAbstract:
        """
        Factory method to create the appropriate ShippingProvider instance 
        based on configuration.
        """
        provider_name = cfg.get("provider_name", "").lower()
        
        # Use dictionary lookup to find the correct class
        provider_class = ShippingWebhookPayloadHandlerFactory._HANDLER_MAP.get(provider_name)

        if provider_class:
            return provider_class() 
        else:
            # Raise a specific, informative exception
            raise UnknownShippingProviderError(
                f"Configuration error: Unknown shipping provider name '{provider_name}'."
            )
