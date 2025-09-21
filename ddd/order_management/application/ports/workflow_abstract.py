from __future__ import annotations
from typing import Protocol

class WorkflowRepositoryAbstract(Protocol):
    def get_next_pending_step(self):
        pass

    def mark_step_done(self, 
            step_name: str, 
            performed_by: str, 
            user_input: dict, 
            executed_at):
        pass

    def all_required_steps_done(self, status: enums.OrderStatus) -> bool:
        pass

    def find_step(self):
        pass
