from __future__ import annotations
# Our own Webhook Sender Service 
import hmac, hashlib
from typing import Mapping
from ddd.order_management.application import ports
from ddd.order_management.domain.services import DomainClock



# Webhook sender service usually have their own headers requirement

# WebhookReceiverAbstract
class WssWebhookReceiver:

    def __init__(self, shared_secret: str, max_age_seconds: int = 3000):
        self.secret = shared_secret
        self.max_age = max_age_seconds

    #def verify(self, headers, body) -> bool:
    def verify(self, headers: Mapping[str, str], raw_body: bytes, request_path: str) -> bool:
        # 1. Normalize all incoming headers to lowercase
        normalized_headers = {k.lower(): v for k, v in headers.items()}
        
        # 2. Extract using lowercase keys (consistent with Lambda Adapter)
        signature = normalized_headers.get("x-wss-signature", "")
        timestamp = normalized_headers.get("x-wss-timestamp", "") #to protect from replay

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
        expected = self.generate_signature(self.secret, raw_body)
        #import pdb;pdb.set_trace()

        return hmac.compare_digest(expected, signature)

    def generate_signature(self, secret: str, body: bytes) -> str:
        signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        return signature