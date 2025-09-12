from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from ddd.order_management.domain import enums
from ddd.order_management.domain.services import DomainClock


@dataclass
class OtherActivity:
    order_id: str
    order_stage: enums.OrderStage
    activity_status: int # workflow status
    sequence: int
    step_name: str
    outcome: enums.StepOutcome
    condition: Optional[str] = None
    performed_by: Optional[str] = None
    user_input: Optional[Dict] = None
    executed_at: Optional[datetime] = None
    optional_step: bool = False

    def mark_as_done(self, performed_by: str, user_input: Optional[Dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE):

        if not performed_by:
            raise exceptions.OtherActivityException(f"performed_by must be provided")

        if not self.is_pending():
            raise exceptions.OtherActivityException(f"Activity {self.step_name} is already finalized {self.outcome}.")

        if self.outcome == outcome:
            raise exceptions.OtherActivityException(f"Activity {self.step_name} is already {outcome}.")

        self.outcome = outcome
        self.performed_by = performed_by
        self.user_input = user_input
        self.executed_at = DomainClock.now()

    def is_pending(self) -> bool:
        return self.outcome in {enums.StepOutcome.WAITING, enums.StepOutcome.HOLD}
