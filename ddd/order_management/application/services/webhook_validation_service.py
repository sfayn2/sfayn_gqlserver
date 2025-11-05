from __future__ import annotations
import json
from typing import Dict

#SIGNATURE_VERIFIER: Dict[str, callable] = {}
#
#def get_verifier_for(provider: str, tenant_id: str) -> Optional[ports.WebhookSignatureVerifier]:
#
#    provider = provider.lower()
#    verifier = SIGNATURE_VERIFIER.get(provider)
#    if verifier:
#        return verifier(tenant_id)
#
#    return None
#
#def validate_webhook(provider, tenant_id, request):
#    verifier = get_verifier_for(provider, tenant_id)
#    if not verifier:
#        raise Exception(f"No verifier found for provider {provider}")
#
#    if not verifier.verify(request.headers, request.body):
#        raise Exception("Invalid signature")
#
#    try:
#        payload = json.loads(request.body.decode())
#    except Exception:
#        raise Exception("Invalid JSON payload")
#
#    payload["tenant_id"] = tenant_id
#
#    return payload

class WebhookValidationService:

    @classmethod
    def configure(cls, saas_service, webhook_receiver_resolver):
        cls.saas_service = saas_service
        cls.webhook_receiver_resolver = webhook_receiver_resolver


    @classmethod
    def _get_provider(cls, tenant_id: str):
        saas_configs = cls.saas_service.get_tenant_config(tenant_id).configs.get("shipping_provider", {})
        return cls.webhook_receiver_resolver.resolve(saas_configs)


    @classmethod
    def validate(cls, tenant_id: str, request):
        #verifier = cls._get_verifier_for_tenant(tenant_id)
        verifier = self._get_provider(tenant_id)

        if not verifier.verify(request.headers, request.body):
            raise Exception("Invalid signature")

        try:
            payload = json.loads(request.body.decode())
        except Exception:
            raise Exception("Invalid JSON payload")

        payload["tenant_id"] = tenant_id

        return payload



