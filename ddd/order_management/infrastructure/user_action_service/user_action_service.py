from __future__ import annotations
import json
from typing import List, Dict, Any, Optional
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
    ) -> Optional[dtos.UserActionDTO]: # Change return type to Optional
        
        # Get the latest object from the database, or None if it doesn't exist
        last_action_log = django_models.UserActionLog.objects.filter(
            order_id=order_id,
            action=action
        ).order_by("-executed_at").first()
        
        # If no action was found, return None immediately
        if last_action_log is None:
            return None

        # Map the single result to the DTO and return it
        return dtos.UserActionDTO(
            order_id=last_action_log.order_id,
            action=last_action_log.action,
            performed_by=last_action_log.performed_by,
            user_input=last_action_log.user_input
        )
