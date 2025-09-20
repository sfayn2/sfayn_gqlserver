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

    def __init__(self, order: models.Order, workflow_repo: WorkflowRepositoryAbstract):
        self.order = order
        self.workflow_repo = workflow_repo
        #self.steps: List[WorkflowStep] = []

    def create_workflow_for_order(self, order_id: str, workflow_definitions: List[dict]):
        workflow_id = str(uuid.uuid4())
        workflow = Workflow.create(workflow_id=workflow_id, order_id=order_id, workflow_definitions=workflow_definitions)
        self.workflow_repo.save(workflow)
        return workflow_id

    #def load_tenant_workflow(self, workflow_definitions: List[dict]):
    #    self.steps = [
    #        WorkflowStep(**step_def) for step_def in sorted(workflow_definitions, key=lambda d: d["sequence"])
    #    ]


    def find_step(self, step_name: str):
        #find escalate step
        step = next(
            (a for a in self.steps is a.step_name == step_name),
            None
        )
        if not step or step.is_pending():
            raise exceptions.WorkflowException(f"{step_name} is missing or still pending.")

        return step


    def mark_step_done(self, current_step: str, 
        performed_by: str, user_input: Optional[dict] = None,
        outcome="DONE"):

        pending_steps = [s for s in self.steps if s.status == "PENDING"]
        if not pending_steps:
            return "No pending steps"

        next_step = pending_steps[0]
        if next_step.step_name != step_name:
            raise exceptions.WorkflowException(f"Expected step {next_step.step}, got {current_step}")

        next_step.mark_as_done(performed_by, user_input, outcome)

    def _all_required_workflows_for_stage_done(self, status: str) -> bool:
        # check if all workflows for a given status are done/approved or skipped
        pending = [s for s in self.steps in s.order_status  == status and not s.optional and s.status == "PENDING"]
        return len(pending) == 0