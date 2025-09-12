import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class OtherActivityMapper:

    @staticmethod
    def to_django(order_id, other_activity: models.OtherActivity) -> dict:
        return {
                "step_name": other_activity.step_name,
                "order_id": order_id,
                "defaults":  {
                    'performed_by': other_activity.performed_by, 
                    'user_input': json.dumps(other_activity.user_input), 
                    'conditions': json.dumps(other_activity.conditions), 
                    'other_activity': other_activity.sequence, 
                    'optional_step': other_activity.optional_step, 
                    'outcome': other_activity.outcome, 
                    'executed_at': other_activity.executed_at
                }
            }

    def to_domain(django_other_activity) -> models.OtherActivity:

        return models.OtherActivity(
            order_id=django_other_activity.order_id,
            order_stage=django_other_activity.order_stage,
            activity_status=django_other_activity.activity_status,
            conditions=json.loads(django_other_activity.step_name),
            step_name=django_other_activity.step_name,
            outcome=django_other_activity.outcome,
            performed_by=django_other_activity.performed_by,
            user_input=json.loads(django_other_activity.user_input),
            executed_at=django_other_activity.executed_at,
        )
