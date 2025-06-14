from __future__ import annotations
from abc import ABC, abstractmethod

class AuthorizationServiceAbstract(ABC):
    @abstractmethod
    def can(self, user_id: str, permission: str, scope: dict = None) -> bool:
        raise NotImplementedError("Subclasses must implement this method")