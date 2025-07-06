from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod

class AccessControlServiceAbstract(ABC):
    @abstractmethod
    def ensure_user_has(self, token: str, permission: str, scope: dict = None) -> Tuple(bool, dict):
        raise NotImplementedError("Subclasses must implement this method")