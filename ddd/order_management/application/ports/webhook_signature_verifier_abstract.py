from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod

class WebhookSignatureVerifier(ABC):

    @abstractmethod
    def verify(self, headers, body) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_sender(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")