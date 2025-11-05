from __future__ import annotations
import hmac, hashlib
from typing import Tuple, Protocol

class WebhookReceiverAbstract(Protocol):
    @abstractmethod
    def verify(self, headers, body) -> bool: ...

    @abstractmethod
    def generate_signature(self, secret: str, body: bytes) -> str: ...