from __future__ import annotations
from typing import Protocol

class WorkflowGatewayAbstract(Protocol):
    def get_next_pending_step(self, order_id: str): ...
    def create_workflow_for_order(self, order_id: str): ...
    def mark_as_done(
        self, 
        order_id: str,
        step_name: str, 
        performed_by: str, 
        user_input: dict, 
        executed_at
    ):
        ...

    def all_required_steps_done(self, order_id: str, status: enums.OrderStatus) -> bool: ...
    def find_step(self, order_id: str, step_name: str): ...