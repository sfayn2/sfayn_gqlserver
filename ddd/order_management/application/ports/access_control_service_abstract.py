from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod

class AccessControlServiceAbstract(ABC):
    @abstractmethod
    def ensure_user_is_authorized_for(
        self, jwt_token: str, required_permission: str, required_scope: dict = None
    ) -> Tuple(bool, dict):
        raise NotImplementedError("Subclasses must implement this method")