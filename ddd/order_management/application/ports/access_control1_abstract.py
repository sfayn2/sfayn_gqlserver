from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod

class AccessControl1Abstract(ABC):
    @abstractmethod
    def ensure_user_is_authorized_for(
        self, token: str, required_permission: str, required_scope: dict = None
    ) -> dtos.UserLoggedInIntegrationEvent:
        raise NotImplementedError("Subclasses must implement this method")