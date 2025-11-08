from __future__ import annotations
import hmac, hashlib
from typing import Tuple, Protocol

class WebhookReceiverAbstract(Protocol):
    def verify(self, headers, body) -> bool: ...
    def generate_signature(self, secret: str, body: bytes) -> str: ...