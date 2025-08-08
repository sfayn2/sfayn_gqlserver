from ddd.order_management.infrastructure import webhook_signatures

def validate_webhook(request):
    verifier = webhook_signatures.get_verifier_for(request.headers)

    if not verifier or not verifier.verify(request.headers, request.body):
        raise Exception("Invalid signature")