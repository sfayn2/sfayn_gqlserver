import hmac, hashlib
from ddd.order_management.application import ports

class GithubSignatureVerifier(ports.WebhookSignatureVerifier):
    def __init__(self, shared_secret: str):
        self.secret = shared_secret.encode()

    def verify(self, headers, body) -> bool:
        signature = headers.get("X-Hub-Signature-256", "")

        if not signature.startswith("sha256="):
            return False

        expected = hmac.new(self.secret, body, hashlib.sha256).hexdigest()

        return hmac.compare_digest(f"sha256={expected}", signature)

    def get_sender(self) -> str:
        return "github"