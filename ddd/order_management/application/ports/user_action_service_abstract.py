from __future__ import annotations
from typing import Protocol

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
    ) -> List[dtos.UserActionDTO]:
        ...