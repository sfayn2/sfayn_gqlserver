from __future__ import annotations
import jmespath
import json
from typing import Dict, Any, Optional
from ddd.order_management.application import ports, dtos, mappers
from .webhook_receiver_factory import WebhookReceiverFactory


# Define custom exceptions for specific error scenarios
class WebhookError(Exception):
    """Base class for webhook processing errors."""
    pass

class ConfigurationError(WebhookError):
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
    saas_lookup_service: Optional[ports.LookupServiceAbstract] = None
    tenant_lookup_service: Optional[ports.LookupServiceAbstract] = None
    webhook_receiver_factory: Optional[WebhookReceiverFactory] = None

    @classmethod 
    def configure(cls, saas_lookup_service, tenant_lookup_service, webhook_receiver_factory):
        cls.saas_lookup_service = saas_lookup_service
        cls.tenant_lookup_service = tenant_lookup_service
        cls.webhook_receiver_factory = webhook_receiver_factory

    @classmethod 
    def _get_provider(cls, tenant_id: str, validator_dto):
        """Internal helper to resolve the correct provider instance."""

        # it satisfies the static analysis tool.
        if cls.saas_lookup_service is None:
            raise RuntimeError("Cannot operate: saas_lookup_service is not configured.")

        if cls.tenant_lookup_service is None:
            raise RuntimeError("Cannot operate: tenant_lookup_service is not configured.")
            
        if cls.webhook_receiver_factory is None:
            raise RuntimeError("Cannot operate: webhook_receiver_factory is not configured.")

            
        try:
            # 1. Type Hinting & Clearer Variable Names
            # Lets turn off tenant source and just get everything from Sass Source; Only Saas Handle Webhook config??
            #tenant_source = cls.tenant_lookup_service.get_tenant_config(tenant_id)
            #saas_source = cls.saas_lookup_service.get_tenant_config(tenant_id)
            
            # Determine the primary source of configuration data
            #config_source = tenant_source.configs if tenant_source and tenant_source.configs else saas_source.configs
            config_source = cls.saas_lookup_service.get_tenant_config(tenant_id)

            if not config_source:
                # 2. Raise a specific custom exception instead of a generic ValueError
                raise ConfigurationError(f"No configuration found for tenant_id: {tenant_id} in both tenant and SaaS lookups.")

            #if webhook_type == 'SHIPMENT_TRACKER':
            #    # Use the specific mapper for shipment configs
            #    config_dto = mappers.ConfigMapper.to_shipment_tracker_config_dto(config_source)
            #elif webhook_type == 'ADD_ORDER':
            #    # Use the specific mapper for order configs
            #    config_dto = mappers.ConfigMapper.to_order_config_dto(config_source)
            #else:
            #    raise ConfigurationError(f"Unknown webhook type: {webhook_type}")
            config_dto = validator_dto(config_source)

            return cls.webhook_receiver_factory.get_webhook_receiver(config_dto)

        except Exception as e:
            raise ConfigurationError(f"Error getting shipment provider {e}")


    @classmethod 
    def validate(cls, tenant_id: str, headers, raw_body, request_path, validator_dto) -> Dict[str, Any]:
        """
        Validates the request signature and decodes the payload.
        """
        ## Determine the webhook type based on the request_path
        #if "/shipment-tracker/" in request_path:
        #    webhook_type = "SHIPMENT_TRACKER"
        #elif "/add-order/" in request_path:
        #    webhook_type = "ADD_ORDER"
        #else:
        #    raise ConfigurationError(f"Cannot determine webhook type from request path: {request_path}")

        # 1. Get the configured verifier instance using the factory dependency
        verifier = cls._get_provider(tenant_id, validator_dto)

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
    def extract_tracking_reference(cls, raw_body: bytes, saas_id: str) -> str:
        """
        Extracts a tracking reference from a raw shipment webhook payload based on
        tenant-specific configuration derived from the 'saas_id'.

        This method assumes the tenant is using the default system webhook structure.
        The SaasLookupService must be configured prior to calling this method.

        Args:
            raw_body: The raw bytes of the webhook payload.
            saas_id: The unique identifier for the SaaS tenant, typically from the request URL.

        Returns:
            The extracted tracking reference as a string.

        Raises:
            RuntimeError: If the saas_lookup_service is not initialized or the
                          tenant configuration is missing/invalid.
            ExtractTrackingError: If the payload is invalid, cannot be parsed,
                                  or the tracking reference cannot be found or is empty.
        """
        if cls.saas_lookup_service is None:
            # Ensures the dependency is present before any work is done.
            raise RuntimeError("Cannot operate: saas_lookup_service is not configured.")

        try:
            # Decode bytes and parse JSON payload
            payload_data: dict[str, Any] = json.loads(raw_body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ExtractTrackingError(f"Invalid JSON payload or encoding: {e}")

        # Attempt to retrieve the SaaSOwner configuration
        saas_config = cls.saas_lookup_service.get_tenant_config(saas_id)

        # Check if the tenant_config was successfully retrieved/is not None
        if not saas_config:
            # Raise an appropriate error if SaaSOwner is not available
            raise RuntimeError(f"SaaS configuration '{saas_id}' is missing or not available.")

        # Proceed with getting the provider name from the configuration
        shipment_provider: Optional[str] = saas_config.configs.get("shipment_shipment_provider")
        tracking_reference: Optional[str] = None # Initialize variable to ensure scope

        tracking_reference = jmespath.search(sass_config.get("shipment_tracking_code_jmespath"), payload_data)


        #if shipment_provider and shipment_provider.lower() == 'easypost':
        #    # EasyPost webhooks often nest the tracker info within an 'result' or 'data' key
        #    tracking_reference = payload_data.get("result", {}).get("tracking_code") or \
        #                         payload_data.get("data", {}).get("tracking_code")
        #else:
        #    # Handle the default case or other providers here if necessary
        #    # e.g., tracking_reference = payload_data.get("default_tracking_key")
        #    pass

        if not tracking_reference:
            # Log the missing key situation for debugging purposes (logging statement omitted for brevity)
            raise ExtractTrackingError(
                f"Tracking reference missing from payload. Attempted paths for provider '{shipment_provider}'."
            )

        # Basic validation that the reference is a non-empty string
        # `isinstance(tracking_reference, str)` check is technically redundant if all paths
        # assign a string or None, but it adds robustness.
        if not isinstance(tracking_reference, str) or not tracking_reference.strip():
            raise ExtractTrackingError("Extracted tracking reference is empty or invalid.")

        return tracking_reference