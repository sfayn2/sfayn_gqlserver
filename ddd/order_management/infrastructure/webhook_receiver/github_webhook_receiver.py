from __future__ import annotations
import hmac, hashlib
from ddd.order_management.domain import exceptions

# Define custom exceptions for specific error scenarios
class MissingHeadersError(exceptions.InvalidOrderOperation):
    """Base class for webhook processing errors."""
    pass

# WebhookReceiverAbstract
class GithubWebhookReceiver:

    def __init__(self, shared_secret: str):
        self.secret = shared_secret.encode()

    def verify(self, headers, body) -> bool:
        normalized_headers = {k.lower(): v for k, v in headers.items()}
        signature = normalized_headers.get("x-hub-signature-256", "")

        if not signature.startswith("sha256="):
            raise MissingHeadersError(f"Required security headers missing: X-Hub-Signature-256."
                                      " Ensure your request includes a valid signature.")

        expected = hmac.new(self.secret, body, hashlib.sha256).hexdigest()

        return hmac.compare_digest(f"sha256={expected}", signature)
