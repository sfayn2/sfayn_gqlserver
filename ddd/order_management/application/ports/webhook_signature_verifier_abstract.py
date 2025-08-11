from __future__ import annotations
import hmac, hashlib
from typing import Tuple
from abc import ABC, abstractmethod

class WebhookSignatureVerifier(ABC):

    @abstractmethod
    def verify(self, headers, body) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def generate_signature(self, secret: str, body: bytes) -> str:
        raise NotImplementedError("Subclasses must implement this method")