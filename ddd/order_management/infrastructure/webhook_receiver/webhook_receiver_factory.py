from __future__ import annotations
from typing import Any, Dict, Type
from datetime import datetime
from ddd.order_management.application import dtos
from .webhook_receiver_abstract import WebhookReceiverAbstract
from .easypost_webhook_receiver import EasyPostWebhookReceiver
from .github_webhook_receiver import GithubWebhookReceiver
from .wss_webhook_receiver import WssWebhookReceiver


# Define a custom exception for better error clarity
class UnknownProviderError(Exception):
    """Raised when the requested webhook provider is unknown."""
    pass

class WebhookReceiverFactory:
    
    # A dictionary mapping provider names (lowercase) to their class constructors
    _RECEIVER_MAP: Dict[str, Any] = {
        "easypost": EasyPostWebhookReceiver,
        "github": GithubWebhookReceiver,
        "wss": WssWebhookReceiver,
    }

    @staticmethod
    def get_webhook_receiver(cfg: dtos.ShipmentWebhookConfigDTO) -> WebhookReceiverAbstract:
        provider = cfg.provider.lower()
        
        # Use dictionary lookup to find the correct class
        receiver_class = WebhookReceiverFactory._RECEIVER_MAP.get(provider)

        if receiver_class:
            # Pass configuration parameters to the constructor dynamically as needed
            # This logic depends on which parameters each class expects
            if provider in ("easypost", "wss"):
                 return receiver_class(
                    shared_secret=cfg.shared_secret,
                    max_age_seconds=cfg.max_age_seconds
                )
            # for others that just need shipment_webhook_shared_secret
            else:
                return receiver_class(
                    shared_secret=cfg.shared_secret
                )
        else:
            # Raise a clear exception if the provider name isn't found
            raise UnknownProviderError(
                f"No webhook receiver found for provider: '{provider}'"
            )

