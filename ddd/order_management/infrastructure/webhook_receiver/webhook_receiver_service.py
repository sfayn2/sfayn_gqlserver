from __future__ import annotations
import json
from typing import Dict, Any, Optional
from ddd.order_management.application import ports
from .webhook_receiver_factory import WebhookReceiverFactory


# Define custom exceptions for specific error scenarios
class WebhookError(Exception):
    """Base class for webhook processing errors."""
    pass

class ExtractTrackingError(WebhookError):
    pass

class InvalidSignatureError(WebhookError):
    """Raised when the signature verification fails (401 Unauthorized)."""
    pass

class InvalidPayloadError(WebhookError):
    """Raised when the JSON payload is invalid (400 Bad Request)."""
    pass

#ports.WebhookReceiverServiceAbstract
class WebhookReceiverService:
    """
    A service responsible for validating and decoding incoming webhook requests.
    """
    saas_service: Optional[ports.TenantServiceAbstract] = None
    webhook_receiver_factory: Optional[WebhookReceiverFactory] = None

    @classmethod 
    def configure(cls, saas_service, webhook_receiver_factory):
        cls.saas_service = saas_service
        cls.webhook_receiver_factory = webhook_receiver_factory

    @classmethod 
    def _get_provider(cls, tenant_id: str):
        """Internal helper to resolve the correct provider instance."""

        # Note: Assuming saas_service methods are robust
        if cls.saas_service is None:
            raise RuntimeError("Cannot get provider: saas_service is not configured.")
            
        # Check the second dependency
        if cls.webhook_receiver_factory is None:
            raise RuntimeError("Cannot get provider: webhook_receiver_factory is not configured.")

        #saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("webhook_provider", {})
        saas_configs = cls.saas_service.get_tenant_config("SaaSOwner").configs.get("webhook_provider", {})
        return cls.webhook_receiver_factory.get_webhook_receiver(saas_configs)

    @classmethod 
    def validate(cls, tenant_id: str, headers, raw_body, request_path) -> Dict[str, Any]:
        """
        Validates the request signature and decodes the payload.
        """
        # 1. Get the configured verifier instance using the factory dependency
        verifier = cls._get_provider(tenant_id)

        # 2. Verify the signature
        #if not verifier.verify(headers=request.headers, raw_body=request.body, request_path=request.path):
        if not verifier.verify(headers=headers, raw_body=raw_body, request_path=request_path):
            # Raise specific error for the API handler to catch and return 401
            raise InvalidSignatureError("Invalid webhook signature")

        # 3. Decode and parse the JSON payload
        try:
            # Assuming body is bytes and should be decoded to UTF-8
            payload = json.loads(raw_body.decode('utf-8')) 
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Raise specific error for the API handler to catch and return 400
            raise InvalidPayloadError("Invalid JSON payload or encoding")
        
        # 4. Enrich the payload with domain data (e.g., tenant_id)
        # This is a common pattern in a service layer
        payload["tenant_id"] = tenant_id

        return payload

    @classmethod
    def extract_tracking_reference(cls, raw_body: bytes) -> str:
        """
        Extracts the tracking reference from the raw webhook body.
        
        This method is static/classmethod as it doesn't depend on an instance state
        and provides a utility function for pre-processing webhooks.

        Args:
            raw_body: The raw bytes received from the webhook producer.
            provider_name: Optional name of the provider (e.g., 'easypost') 
                           to use provider-specific logic.

        Raises:
            ExtractTrackingError: If the payload is invalid or the reference is missing.
        """
        try:
            # Decode bytes and parse JSON payload
            payload_data = json.loads(raw_body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ExtractTrackingError(f"Invalid JSON payload or encoding: {e}")
        
        # Use provider-specific logic if available
        # TODO: SaaSOwner meands default or applyies for all; should apply to all Tenants
        if cls.saas_service:
            provider_name = cls.saas_service.get_tenant_config("SaaSOwner").configs.get("webhook_provider", {}).get("name")
            if provider_name and provider_name.lower() == 'easypost':
                # EasyPost webhooks often nest the tracker info within an 'result' or 'data' key
                tracking_reference = payload_data.get("result", {}).get("tracking_code") or \
                                    payload_data.get("data", {}).get("tracking_code")
        else:
            # Fallback for generic or unknown providers
            tracking_reference = payload_data.get("tracking_code") or \
                                 payload_data.get("id") # sometimes the main ID is the tracking ref

        if not tracking_reference:
            # Log the missing key situation for debugging purposes
            raise ExtractTrackingError(f"Tracking reference missing from payload. Attempted paths for provider '{provider_name}'.")

        # Basic validation that the reference is a non-empty string
        if not isinstance(tracking_reference, str) or not tracking_reference.strip():
            raise ExtractTrackingError("Extracted tracking reference is empty or invalid.")

        return tracking_reference 