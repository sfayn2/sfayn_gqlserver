from __future__ import annotations
from typing import Protocol, Optional
from ddd.order_management.application import dtos

class UserActionServiceAbstract(Protocol):
    def save_action(
        self,
        user_action_data: dtos.UserActionDTO
    ) -> None:
        ...

    def get_last_action(
        self,
        order_id: str,
        action: str
    ) -> Optional[dtos.UserActionDTO]: # Change return type to Optional
        ...