from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

#Protocol: ports.UserActionServiceAbstract
class UserActionService:
    def save_action(
        self,
        user_action_data: dtos.UserActionDTO
    ) -> None:
        django_models.UserActionLog.objects.create(
            order_id=user_action_data.order_id,
            action=user_action_data.action,
            performed_by=user_action_data.performed_by,
            user_input=user_action_data.user_input
        )

    def get_last_action(
        self,
        order_id: str,
        action: str
    ) -> List[dtos.UserActionDTO]:
        return [
            dtos.UserActionDTO(
                order_id=dj_user_action.order_id,
                action=dj_user_action.action,
                performed_by=dj_user_action.performed_by,
                user_input=dj_user_action.user_input
            )
            for dj_user_action in django_models.UserActionLog.objects.filter(
                order_id=order_id,
                action=action
            ).order_by("-executed_at")
        ]
