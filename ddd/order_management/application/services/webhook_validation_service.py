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
    def configure(cls, saas_service, signature_verifier):
        cls.saas_service = saas_service
        cls.signature_verifier = signature_verifier

    @classmethod
    def _get_verifier_for_tenant(cls, tenant_id: str):
        saas_config = cls.saas_service.get_tenant_config(tenant_id)
        shared_secret = saas_config.configs.get("webhook_secret", {})
        if not shared_secret:
            raise Exception(f"No webhook secret configured for tenant {tenant_id}")

        return cls.signature_verifier(shared_secret)


    @classmethod
    def validate(cls, tenant_id: str, request):
        verifier = cls._get_verifier_for_tenant(tenant_id)

        if not verifier.verify(request.headers, request.body):
            raise Exception("Invalid signature")

        try:
            payload = json.loads(request.body.decode())
        except Exception:
            raise Exception("Invalid JSON payload")

        payload["tenant_id"] = tenant_id

        return payload



