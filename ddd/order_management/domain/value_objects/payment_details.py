from __future__ import annotations
from dataclasses import dataclass
from ddd.order_management.domain import enums, exceptions
from decimal import Decimal
from .money import Money

@dataclass(frozen=True)
class PaymentDetails:
    order_id: str
    method: str
    paid_amount: Money
    transaction_id: str
    status: str

    def __post_init__(self):
        if not self.order_id:
            raise exceptions.PaymentDetailsException("Order Id in is required for 3rd Party payment verification.")

        if not self.method:
            raise exceptions.PaymentDetailsException("Payment method is required.")

        if not self.paid_amount:
            raise exceptions.PaymentDetailsException("Paid amount is required.")

        if not self.status:
            raise exceptions.PaymentDetailsException("Payment status is required.")

        if not self.method.value in [item.value for item in enums.PaymentMethod]:
            raise exceptions.PaymentDetailsException(f"Payment method {self.method.value} not supported.")

        if self.paid_amount and self.paid_amount.amount < Decimal("0"):
            raise exceptions.PaymentDetailsException("Paid amount cannot be negative.")

        if not self.method != enums.PaymentMethod.COD and not self.transaction_id:
            raise exceptions.PaymentDetailsException("Transaction ID is required for non-COD payments.")

