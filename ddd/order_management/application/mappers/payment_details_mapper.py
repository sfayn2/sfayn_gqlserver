from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class PaymentDetailsMapper:

    @staticmethod
    def to_domain(payment_details_dto: dtos.PaymentDetailsDTO) -> value_objects.PaymentDetails:
        return value_objects.PaymentDetails(
            order_id=payment_details_dto.order_id,
            method=payment_details_dto.method,
            paid_amount=value_objects.Money(
                amount=payment_details_dto.paid_amount.amount,
                currency=payment_details_dto.paid_amount.currency
            ),
            transaction_id=payment_details_dto.transaction_id,
            status=payment_details_dto.status
        )