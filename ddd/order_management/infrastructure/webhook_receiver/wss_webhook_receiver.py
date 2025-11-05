from __future__ import annotations
# Our own Webhook Sender Service 
import hmac, hashlib
from ddd.order_management.application import ports
from ddd.order_management.domain.services import DomainClock



# Webhook sender service usually have their own headers requirement

# WebhookReceiverAbstract
class WssWebhookReceiver:

    def __init__(self, shared_secret: str, max_age: int = 3000):
        self.secret = shared_secret
        self.max_age = max_age

    def verify(self, headers, body) -> bool:
        signature = headers.get("X-Wss-Signature", "")
        timestamp = headers.get("X-Wss-Timestamp", "") #to protect from replay
        if not signature or not timestamp:
            return False

        # check freshness
        try:
            ts = int(timestamp)
            if abs(DomainClock.now().timestamp() - ts) >= self.max_age:
                return False
        except ValueError:
            return False

        # recompute signature
        expected = self.generate_signature(self.secret, body)
        #import pdb;pdb.set_trace()

        return hmac.compare_digest(expected, signature)

    def generate_signature(self, secret: str, body: bytes) -> str:
        signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        return signature