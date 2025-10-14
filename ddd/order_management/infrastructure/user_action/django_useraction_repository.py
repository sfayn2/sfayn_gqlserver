from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums

#Protocol: ports.UserActionLogAbstract
class DjangoUserActionRepository:
    def save_action(
        self,
        order_id,
        action,
        performed_by,
        user_input
    ):
        django_models.UserActionLog.objects.create(
            order_id=order_id,
            action=action,
            performed_by=performed_by,
            user_input=user_input
        )

    def get_last_action(
        self,
        order_id,
        action
    ):
        return django_models.UserActionLog.objects.filter(
            order_id=order_id,
            action=action
        )
