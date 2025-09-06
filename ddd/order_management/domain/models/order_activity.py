from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from ddd.order_management.domain import enums
from ddd.order_management.domain.services import DomainClock


@dataclass
class OrderActivity:
    order_id: str
    order_status: int # workflow status
    sequence: int
    step: str
    step_status: enums.StepStatus
    performed_by: Optional[str] = None
    user_input: Optional[Dict] = None
    executed_at: Optional[datetime] = None
    optional_step: bool = False


    def mark_as_done(self):
        if not self.is_pending:
            raise exceptions.OrderActivityException(f"Order Activity {self.step} is already done.")
        self.step_status = enums.StepStatus.DONE
        self.performed_by = performed_by
        self.user_input = user_input
        self.executed_at = DomainClock.now()

    def is_pending(self) -> bool:
        return self.step_status in {enums.StepStatus.WAITING, enums.StepStatus.OPTIONAL}
