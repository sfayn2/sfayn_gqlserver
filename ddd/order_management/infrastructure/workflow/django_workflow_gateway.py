from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums

#Protocol: ports.WorkflowGatewayAbstract
class DjangoWorkflowGateway:
    def __init__(self, default_workflow: List[Dict[str, Any]]):
        self.default_workflow = default_workflow

    def get_workflow_definition(self) -> List[dict]:
        steps = []
        tenant_workflow_definition = django_models.WorkflowDefinition.objects.filter(tenant_id=self.order.tenant_id)
        if not tenant_workflow_definition.exists():
            return self.default_workflow

        for row in tenant_workflow_definition:
            steps.append(
                dict(
                    order_status=row.order_status,
                    workflow_status=row.workflow_status,
                    step_name=row.step_name,
                    conditions=json.loads(row.conditions or "{}"),
                    sequence=row.sequence,
                    optional_step=row.optional_step
                )
            )
        return steps

    def create_workflow_for_order(self, order_id: str):
        workflow_definitions = self.get_workflow_definition()
        for step in sorted(workflow_definitions, key=lambda d: d["sequence"]):
            django_models.WorkflowExecution.objects.create(
                order_id=order_id,
                order_status=step["order_status"],
                sequence=step["sequence"],
                step_name=step["step_name"],
                outcome=enums.StepOutcome.WAITING,
                optional_step=step["optional_step"],
                conditions=step["conditions"]
            )


    def get_next_pending_step(self, order_id: str):
        step_obj = django_models.WorkflowExecution.objects.filter(
            order_id=order_id,
            outcome=enums.StepOutcome.WAITING,
            sequence__isnull=False
        ).order_by("sequence").first()

        if not step_obj:
            return None

        return step_obj


    def mark_as_done(
        self, 
        order_id: str,
        step_name: str, 
        performed_by: str, 
        user_input: dict, 
        executed_at
    ):
        django_models.WorkflowExecution.objects.filter(
            order_id=order_id,
            step_name=step_name,
        ).update(
            outcome=enums.StepOutcome.DONE,
            performed_by=performed_by,
            user_input=json.dumps(user_input),
            executed_at=executed_at
        )

    def all_required_steps_done(self, order_id: str, status: enums.OrderStatus) -> bool:
        with_pending_steps = django_models.WorkflowExecution.objects.filter(
            order_id=order_id,
            order_status=status.value,
            outcome=enums.StepOutcome.WAITING
        )

        if with_pending_steps.exists():
            raise exceptions.InvalidOrderOperation(f"Unable to proceed, some workflows in statuses are still pending.")

        return True

    def find_step(self, order_id: str, step_name: str, outcome: enums.StepOutcome = enums.StepOutcome.DONE):
        try:
            return django_models.WorkflowExecution.objects.get(
                order_id=order_id,
                step_name=step_name,
                outcome=enums.StepOutcome.DONE
            )
        except django_models.WorkflowExecution.DoesNotExists:
            raise exceptions.WorkflowException(f"Step '{step_name}' not found for order '{order_id}' ")


