import json, jmespath
from typing import Any, Optional
from ddd.order_management.application import ports

class ExtractTrackingError(Exception):
    pass

class ConfigurationError(Exception):
    pass


#ports.TrackingReferenceExtractorAbstract implementation for API Gateway
class TrackingReferenceExtractor:

    """
    A service responsible for validating and decoding incoming webhook requests.
    """
    saas_lookup_service: Optional[ports.LookupServiceAbstract] = None

    @classmethod 
    def configure(cls, saas_lookup_service):
        cls.saas_lookup_service = saas_lookup_service

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
        if not saas_config or not saas_config.configs:
            # Raise an appropriate error if SaaSOwner is not available
            raise RuntimeError(f"SaaS configuration '{saas_id}' is missing or not available.")

        # Proceed with getting the provider name from the configuration
        webhook_shipment_config = saas_config.configs.get("webhooks", {}).get("shipment_tracker", {})
        shipment_provider: Optional[str] = webhook_shipment_config.get("provider")
        tracking_reference: Optional[str] = None # Initialize variable to ensure scope

        jmespath_expr = webhook_shipment_config.get("tracking_reference_jmespath")
        if not jmespath_expr:
            raise ConfigurationError("Missing JMESPath config: tracking_reference_jmespath")

        tracking_reference = jmespath.search(jmespath_expr, payload_data)

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