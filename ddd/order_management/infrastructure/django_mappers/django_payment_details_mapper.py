import ast
from ddd.order_management.domain import models, value_objects, enums

class PaymentDetailsMapper:

    @staticmethod
    def to_domain(payment_object) -> value_objects.PaymentDetails:
        return  value_objects.PaymentDetails(
                order_id=payment_object.order_id,
                method=payment_object.payment_method,
                transaction_id=payment_object.payment_reference,
                paid_amount=value_objects.Money(
                    amount=payment_object.payment_amount,
                    currency=payment_object.currency
                ),
                status=enums.PaymentStatus(payment_object.payment_status)
        )