from __future__ import annotations
from typing import Protocol
import json
from order_management import models as django_models

class WorkflowExecutionRepositoryAbstract(Protocol):
    def get_next_pending_step(self, status: enums.OrderStatus):
        pass

    def mark_step_done(self, 
            step_name: str, 
            performed_by: str, 
            user_input: dict, 
            executed_at):
        pass

    def all_required_steps_done(self, order_id: str, status: enums.OrderStatus) -> bool:
        pass


class WorkflowExecutionRepository:
    def __init(self, order_id: str):
        self.order_id = order_id

    def get_next_pending_step(self, status: enums.OrderStatus):
        return django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            order_status=status.value,
            status="PENDING"
        ).order_by("sequence").first()

    def mark_step_done(self, 
            step_name: str, 
            performed_by: str, 
            user_input: dict, 
            executed_at):
        django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            step_name=step_name,
        ).update(
            status="DONE",
            performed_by=performed_by,
            user_input=json.dumps(user_input),
            executed_at=executed_at
        )

    def all_required_steps_done(self, order_id: str, status: enums.OrderStatus) -> bool:
        return not django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            order_status=status.value,
            status="PENDING"
        ).exists()