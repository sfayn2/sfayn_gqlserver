from __future__ import annotations
from typing import Tuple, Optional, Protocol, Any
from ddd.order_management.application import dtos

class AccessControl1Abstract(Protocol):
    def __init__(self, jwt_handler: Any) -> None: ...
    def get_user_context(self, token: str, request_tenant_id: str) -> dtos.UserContextDTO: ...
    def ensure_user_is_authorized_for(
        self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
    ) -> bool: ...