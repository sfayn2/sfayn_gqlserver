from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

class WorkflowService:

    def __init__(self, workflow_repo: WorkflowRepositoryAbstract):
        self.workflow_repo = workflow_repo

    def create_workflow_for_order(self, order_id: str):
        self.workflow_repo.create_workflow_for_order(order_id)

    def get_step(self, step_name: str):
        step = self.workflow_repo.find_step(step_name)
        if not step:
            raise exceptions.WorkflowException(f"Step {step_name} not found for {self.order_id}")
        return self._to_dto(step)

    def mark_step_done(
        self, 
        current_step: str, 
        performed_by: str, 
        user_input: Optional[dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE
    ):

        pending_step = self.workflow_repo.get_next_pending_step()
        if not pending_step:
            raise exceptions.WorkflowException(f"No pending steps")

        if pending_step.step_name != step_name:
            raise exceptions.WorkflowException(f"Expected step {pending_step.step_name}, got {step_name}")

        self.workflow_repo.mark_as_done(
            step_name=step_name,
            performed_by=performed_by, 
            user_input=user_input, 
            out_come=outcome
        )

    def all_required_workflows_for_stage_done(self, status: enums.OrderStatus) -> bool:
        return self.workflow_repo.all_required_steps_done(status)

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