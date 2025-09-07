import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class OrderActivityMapper:

    @staticmethod
    def to_django(order_id, order_activity: models.OrderActivity) -> dict:
        return {
                "step": order_activity.step,
                "order_id": order_id,
                "defaults":  {
                    'performed_by': order_activity.performed_by, 
                    'user_input': json.dumps(order_activity.user_input), 
                    'order_activity': order_activity.sequence, 
                    'optional_step': order_activity.optional_step, 
                    'step_status': order_activity.step_status, 
                    'executed_at': order_activity.executed_at
                }
            }

    def to_domain(django_order_activity) -> models.OrderActivity:

        return models.OrderActivity(
            order_id=django_order_activity.order_id,
            activity_status=django_order_activity.activity_status,
            step=django_order_activity.step,
            step_status=django_order_activity.step_status,
            performed_by=django_order_activity.performed_by,
            user_input=json.loads(django_order_activity.user_input),
            executed_at=django_order_activity.executed_at,
        )
