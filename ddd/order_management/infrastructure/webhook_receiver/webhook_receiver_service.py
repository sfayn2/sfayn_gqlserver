from __future__ import annotations
import json
from typing import Dict, Any


# Define custom exceptions for specific error scenarios
class WebhookError(Exception):
    """Base class for webhook processing errors."""
    pass

class InvalidSignatureError(WebhookError):
    """Raised when the signature verification fails (401 Unauthorized)."""
    pass

class InvalidPayloadError(WebhookError):
    """Raised when the JSON payload is invalid (400 Bad Request)."""
    pass

class WebhookReceiverService:
    """
    A service responsible for validating and decoding incoming webhook requests.
    """

    @classmethod 
    def configure(cls, saas_service, webhook_receiver_factory):
        cls.saas_service = saas_service
        cls.webhook_receiver_factory = webhook_receiver_factory

    @classmethod 
    def _get_provider(cls, tenant_id: str):
        """Internal helper to resolve the correct provider instance."""
        # Note: Assuming saas_service methods are robust
        saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("webhook_provider", {})
        return cls.webhook_receiver_factory.get_webhook_receiver(saas_configs)

    @classmethod 
    def validate(cls, tenant_id: str, request) -> Dict[str, Any]:
        """
        Validates the request signature and decodes the payload.
        """
        # 1. Get the configured verifier instance using the factory dependency
        verifier = cls._get_provider(tenant_id)

        # 2. Verify the signature
        if not verifier.verify(request.headers, request.body):
            # Raise specific error for the API handler to catch and return 401
            raise InvalidSignatureError("Invalid webhook signature")

        # 3. Decode and parse the JSON payload
        try:
            # Assuming body is bytes and should be decoded to UTF-8
            payload = json.loads(request.body.decode('utf-8')) 
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Raise specific error for the API handler to catch and return 400
            raise InvalidPayloadError("Invalid JSON payload or encoding")
        
        # 4. Enrich the payload with domain data (e.g., tenant_id)
        # This is a common pattern in a service layer
        payload["tenant_id"] = tenant_id

        return payload
