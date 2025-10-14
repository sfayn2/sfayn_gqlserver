from __future__ import annotations
from typing import Protocol

class UserActionAbstract(Protocol):
    def save_action(
        self,
        order_id,
        action,
        performed_by,
        user_input
    ):
        ...

    def get_last_action(
        self,
        order_id,
        action
    ):
        ...