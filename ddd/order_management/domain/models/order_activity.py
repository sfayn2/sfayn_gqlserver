from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from ddd.order_management.domain import enums
from ddd.order_management.domain.services import DomainClock


@dataclass
class OrderActivity:
    order_id: str
    activity_status: int # workflow status
    sequence: int
    step: str
    outcome: enums.StepOutcome
    performed_by: Optional[str] = None
    user_input: Optional[Dict] = None
    executed_at: Optional[datetime] = None
    optional_step: bool = False


    def mark_as_done(self, performed_by: str, user_input: Optional[dict] = None):
        if self.outcome == enums.StepOutcome.DONE:
            raise exceptions.OrderActivityException(f"Order Activity {self.step} is already done.")
        self.outcome = enums.StepOutcome.DONE
        self.performed_by = performed_by
        self.user_input = user_input
        self.executed_at = DomainClock.now()

    def mark_as_approved(self, performed_by: str, user_input: Optional[dict] = None):
        if self.outcome == enums.StepOutcome.APPROVED:
            raise exceptions.OrderActivityException(f"Order Activity {self.step} is already approved.")
        self.outcome = enums.StepOutcome.APPROVED
        self.performed_by = performed_by
        self.user_input = user_input
        self.executed_at = DomainClock.now()

    def mark_as_rejected(self, performed_by: str, user_input: Optional[dict] = None):
        if self.outcome == enums.StepOutcome.REJECTED:
            raise exceptions.OrderActivityException(f"Order Activity {self.step} is already rejected.")
        self.outcome = enums.StepOutcome.REJECTED
        self.performed_by = performed_by
        self.user_input = user_input
        self.executed_at = DomainClock.now()

    def is_pending(self) -> bool:
        return self.outcome in {enums.StepOutcome.WAITING, enums.StepOutcome.REJECTED}
