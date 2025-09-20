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

    def all_required_steps_done(self, status: enums.OrderStatus) -> bool:
        pass

    def get_step(self):
        pass


class WorkflowExecutionRepository:
    def __init(self, order_id: str):
        self.order_id = order_id

    def create_workflow_for_order(self, order_id: str, workflow_definition: List[dict]):
        for i, step in enumerate(sorted(workflow_definitions, key=lambda d: d["sequence"])):
            django_models.WorkflowExecution.objects.create(
                order_id=order_id,
                order_status=step["order_status"],
                sequence=step["sequence"],
                step_name=step["step_name"],
                outcome=enums.StepOutcome.WAITING,
                optional_step=step["optional_step"],
                condition=step["condition"]
            )


    def get_next_pending_step(self):
        step_obj = django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            status=enums.StepOutcome.PENDING
        ).order_by("sequence").first()

        if not step_obj:
            return None

        return self._to_dto(step_obj)


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

    def all_required_steps_done(self, status: enums.OrderStatus) -> bool:
        return not django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            order_status=status.value,
            status=enums.StepOutcome.WAITING
        ).exists()

    def get_step(self):
        step_obj = django_models.WorkflowExecution.objects.filter(
            order_id=self.order_id,
            status=enums.StepOutcome.DONE
        ).order_by("sequence").first()

        if not step_obj:
            return None

        return self._to_dto(step_obj)


    def _to_dto(self, step_obj) -> dtos.WorkflowStepDTO:
        return dtos.WorkflowStepDTO(
            order_id=step_obj.order_id,
            order_status=step_obj.order_status,
            sequence=step_obj.sequence,
            step_name=step_obj.step_name,
            outcome=step_obj.outcome,
            conditions=json.loads(step_obj.conditions),
            performed_by=step_obj.performed_by,
            user_input=json.loads(step_obj.user_input) if step_obj.user_input else None,
            executed_at=step_obj.executed_at,
            optional_step=step_obj.optional_step


        )