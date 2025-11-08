from __future__ import annotations
from typing import Tuple, Optional, Protocol

class AccessControl1Abstract(Protocol):
    def get_user_context(self, token: str) -> dtos.UserContextDTO: ...
    def ensure_user_is_authorized_for(
        self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
    ) -> dtos.UserContextDTO: ...