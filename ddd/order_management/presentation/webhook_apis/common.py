import json
from ddd.order_management.infrastructure import webhook_signatures

def validate_webhook(provider, tenant_id, request):
    verifier = webhook_signatures.get_verifier_for(provider, tenant_id, request.headers)
    if not verifier:
        raise Exception(f"No verifier found for provider {provider}")

    if not verifier.verify(request.headers, request.body):
        raise Exception("Invalid signature")

    try:
        payload = json.loads(request.body.decode())
    except Exception:
        raise Exception("Invalid JSON payload")

    payload["tenant_id"] = tenant_id

    return payload