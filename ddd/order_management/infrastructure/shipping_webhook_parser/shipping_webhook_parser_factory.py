from __future__ import annotations
from typing import Any, Optional, Dict, Type
from datetime import datetime
from ddd.order_management.application import dtos
from .shipping_webhook_parser_abstract import ShippingWebhookParserAbstract
from .easypost_shipping_webhook_parser import EasyPostShippingWebhookParser


# Define a custom exception for better error clarity
class UnknownShippingProviderError(Exception):
    """Raised when the requested shipping provider name is unknown."""
    pass


class ShippingWebhookParserFactory:

    # A dictionary mapping provider names (lowercase for consistency) to their classes
    _PARSER_MAP: Dict[str, Type[ShippingWebhookParserAbstract]] = {
        "easypost": EasyPostShippingWebhookParser,
    }
    
    @staticmethod
    def get_payload_parser(cfg: dtos.ShipmentWebhookConfigDTO) -> ShippingWebhookParserAbstract:
        """
        Factory method to create the appropriate ShippingProvider instance 
        based on configuration.
        """
        shipment_provider = cfg.provider.lower()
        
        # Use dictionary lookup to find the correct class
        provider_class = ShippingWebhookParserFactory._PARSER_MAP.get(shipment_provider)

        if provider_class:
            return provider_class() 
        else:
            # Raise a specific, informative exception
            raise UnknownShippingProviderError(
                f"Configuration error: Unknown shipping provider name '{shipment_provider}'."
            )
