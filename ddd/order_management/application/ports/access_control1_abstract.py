from __future__ import annotations
from typing import Tuple, Optional
from abc import ABC, abstractmethod

class AccessControl1Abstract(ABC):
    @abstractmethod
    def get_user_context(self, token: str) -> dtos.UserContextDTO:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def ensure_user_is_authorized_for(
        self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
    ) -> dtos.UserContextDTO:
        raise NotImplementedError("Subclasses must implement this method")