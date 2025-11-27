from __future__ import annotations
import hmac, hashlib

# WebhookReceiverAbstract
class GithubWebhookReceiver:

    def __init__(self, shared_secret: str):
        self.secret = shared_secret.encode()

    def verify(self, headers, body) -> bool:
        signature = headers.get("X-Hub-Signature-256", "")

        if not signature.startswith("sha256="):
            return False

        expected = hmac.new(self.secret, body, hashlib.sha256).hexdigest()

        return hmac.compare_digest(f"sha256={expected}", signature)
