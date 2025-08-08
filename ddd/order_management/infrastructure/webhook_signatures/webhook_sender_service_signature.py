# Our own Webhook Sender Service 
import hmac, hashlib
from ddd.order_management.application import ports

class WSSSignatureVerifier(ports.WebhookSignatureVerifier):
    def __init__(self, shared_secret: str, max_age: int = 300):
        self.secret = shared_secret.encode()
        self.max_age = max_age

    def verify(self, headers, body) -> bool:
        signature = headers.get("X-WSS-Signature", "")
        timestamp = headers.get("X-WSS-Timestamp", "") #to protect from replay

        if not signature or not timestamp:
            return False

        # check freshness
        try:
            ts = int(timestamp)
            if abs(int(time.time()) - ts) >= self.max_age:
                return False
        except ValueError:
            return False

        # recompute signature
        message = f"{timestamp}.{body.decode()}".encode()
        expected = hmac.new(self.secret, message, hashlib.sha256).hexdigest()

        return hmac.compare_digest(f"sha256={expected}", signature)

    def get_sender(self) -> str:
        return "webhook_sender_service"