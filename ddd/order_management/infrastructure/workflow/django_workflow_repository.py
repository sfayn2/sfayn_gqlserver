from __future__ import annotations
import json
from order_management import models as django_models


class DjangoWorkflowRepository:
    def __init__(self, order: models.Order):
        self.order = order

    def get_workflow_definition(self) -> List[dict]:
        steps = []
        for row in django_models.WorkflowDefinition.objects.filter(tenant_id=self.order.tenant_id):
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
        for i, step in enumerate(sorted(workflow_definitions, key=lambda d: d["sequence"])):
            django_models.WorkflowExecution.objects.create(
                order_id=self.order.order_id,
                order_status=step["order_status"],
                sequence=step["sequence"],
                step_name=step["step_name"],
                outcome=enums.StepOutcome.WAITING,
                optional_step=step["optional_step"],
                conditions=step["conditions"]
            )


    def get_next_pending_step(self):
        step_obj = django_models.WorkflowExecution.objects.filter(
            order_id=self.order.order_id,
            outcome=enums.StepOutcome.WAITING
        ).order_by("sequence").first()

        if not step_obj:
            return None

        return step_obj


    def mark_as_done(self, 
            step_name: str, 
            performed_by: str, 
            user_input: dict, 
            executed_at):
        django_models.WorkflowExecution.objects.filter(
            order_id=self.order.order_id,
            step_name=step_name,
        ).update(
            status=enums.StepOutcome.DONE,
            performed_by=performed_by,
            user_input=json.dumps(user_input),
            executed_at=executed_at
        )

    def all_required_steps_done(self, status: enums.OrderStatus) -> bool:
        return not django_models.WorkflowExecution.objects.filter(
            order_id=self.order.order_id,
            order_status=status.value,
            outcome=enums.StepOutcome.WAITING
        ).exists()

    def find_step(self, step_name: str):
        step_obj = django_models.WorkflowExecution.objects.filter(
            order_id=self.order.order_id,
            step_name=step_name,
            status=enums.StepOutcome.DONE
        ).order_by("sequence").first()

        if not step_obj:
            return None

        return step_obj

