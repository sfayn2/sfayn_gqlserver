from ddd.order_management.infrastructure import webhook_signatures

def validate_webhook(provider, tenant_id, request):
    verifier = webhook_signatures.get_verifier_for(provider, tenant_id, request.headers)

    if not verifier or not verifier.verify(request.headers, request.body):
        raise Exception("Invalid signature")

    try:
        payload = json.loads(body.decode())
    except Exception:
        raise Exception("Invalid JSON")

    payload["tenant_id"] = tenant_id

    return payload