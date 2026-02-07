from __future__ import annotations
import jmespath
import json
from typing import Dict, Any, Optional, Callable
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


# Define a type alias for the expected signature of the validator function
ValidatorFunc = Callable[[Dict[str, Any]], dtos.WebhookReceiverConfigDTO]

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
    def _get_provider(cls, tenant_id: str, validator_dto: ValidatorFunc):
        """Internal helper to resolve the correct provider instance."""

        # it satisfies the static analysis tool.
        if cls.saas_lookup_service is None:
            raise RuntimeError("Cannot operate: saas_lookup_service is not configured.")

        if cls.tenant_lookup_service is None:
            raise RuntimeError("Cannot operate: tenant_lookup_service is not configured.")
            
        if cls.webhook_receiver_factory is None:
            raise RuntimeError("Cannot operate: webhook_receiver_factory is not configured.")

        try:
            #SaaS Owner should own the tenant webhook configuration?
            config_source = cls.saas_lookup_service.get_tenant_config(tenant_id)

            if not config_source:
                # 2. Raise a specific custom exception instead of a generic ValueError
                raise ConfigurationError(f"No configuration found for tenant_id: {tenant_id} in SaaS lookups.")

            webhook_config = config_source.configs.get("webhooks", {})
            if not webhook_config:
                raise ConfigurationError(f"No webhooks configuration found for tenant_id: {tenant_id} in SaaS lookups.")
            
            config_dto: dtos.WebhookReceiverConfigDTO = validator_dto(webhook_config)

            return cls.webhook_receiver_factory.get_webhook_receiver(config_dto)

        except Exception as e:
            raise ConfigurationError(f"Error getting shipment provider {e}")


    @classmethod 
    def validate_signature(cls, tenant_id: str, headers, raw_body, request_path, validator_dto: ValidatorFunc) -> Dict[str, Any]:
        """
        Validates the request signature and decodes the payload.
        """

        # 1. Get the configured verifier instance using the factory dependency
        verifier = cls._get_provider(tenant_id, validator_dto)

        # 2. Verify the signature
        #if not verifier.verify(headers=request.headers, raw_body=request.body, request_path=request.path):
        if not verifier.verify(headers=headers, raw_body=raw_body, request_path=request_path):
            # Raise specific error for the API handler to catch and return 401
            raise InvalidSignatureError("Invalid webhook signature or SaSS/Tenant Configurator is not setup properly")

