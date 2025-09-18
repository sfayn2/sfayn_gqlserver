import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class WorkflowMapper:

    @staticmethod
    def to_django(order_id, workflow: models.Workflow) -> dict:
        return {
                "step_name": workflow.step_name,
                "order_id": order_id,
                "defaults":  {
                    'performed_by': workflow.performed_by, 
                    'user_input': json.dumps(workflow.user_input), 
                    'conditions': json.dumps(workflow.conditions), 
                    'workflow': workflow.sequence, 
                    'optional_step': workflow.optional_step, 
                    'outcome': workflow.outcome, 
                    'executed_at': workflow.executed_at
                }
            }

    def to_domain(django_workflow) -> models.Workflow:

        return models.Workflow(
            order_id=django_workflow.order_id,
            order_stage=django_workflow.order_stage,
            activity_status=django_workflow.activity_status,
            conditions=json.loads(django_workflow.step_name),
            step_name=django_workflow.step_name,
            outcome=django_workflow.outcome,
            performed_by=django_workflow.performed_by,
            user_input=json.loads(django_workflow.user_input),
            executed_at=django_workflow.executed_at,
        )
