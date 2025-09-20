from typing import Optional, Protocol
from dataclasses import dataclass
from ddd.order_management.domain import enums
from ddd.order_management.domain.services import DomainClock


#@dataclass
#class WorkflowStep:
#    order_id: str
#    order_status: enums.OrderStatus
#    sequence: int
#    step_name: str
#    outcome: enums.StepOutcome
#    condition: Optional[str] = None
#    performed_by: Optional[str] = None
#    user_input: Optional[Dict] = None
#    executed_at: Optional[datetime] = None
#    optional_step: bool = False
#
#    def mark_as_done(self, performed_by: str, user_input: Optional[Dict] = None,
#        outcome: enums.StepOutcome = enums.StepOutcome.DONE):
#
#        if not performed_by:
#            raise exceptions.WorkflowException(f"performed_by must be provided")
#
#        if not self.is_pending():
#            raise exceptions.WorkflowException(f"Workflow {self.step_name} is already finalized {self.outcome}.")
#
#        if self.outcome == outcome:
#            raise exceptions.WorkflowException(f"Workflow {self.step_name} is already {outcome}.")
#
#        self.outcome = outcome
#        self.performed_by = performed_by
#        self.user_input = user_input
#        self.executed_at = DomainClock.now()
#
#    def is_pending(self) -> bool:
#        return self.outcome in {enums.StepOutcome.WAITING, enums.StepOutcome.HOLD}



class WorkflowService:

    def __init__(self, workflow_repo: WorkflowRepositoryAbstract):
        self.workflow_repo = workflow_repo

    def create_workflow_for_order(self, order_id: str, workflow_definitions: List[dict]):
        self.workflow_repo.create_workflow_for_order(order_id, workflow_definition)

    def get_step(self, step_name: str):
        return self.workflow_repo.get_step(step_name)

    def mark_step_done(self, current_step: str, 
        performed_by: str, user_input: Optional[dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE):

        pending_step = self.workflow_repo.get_next_pending_step()
        if not pending_step:
            return "No pending steps"

        if pending_step.step_name != step_name:
            raise exceptions.WorkflowException(f"Expected step {pending_step.step_name}, got {step_name}")

        self.workflow_repo.mark_as_done(performed_by, user_input, outcome)

    def all_required_workflows_for_stage_done(self, status: str) -> bool:
        return self.workflow_repo.all_required_steps_done(status)