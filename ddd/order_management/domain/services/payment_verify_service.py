import requests
from decimal import Decimal
from typing import Tuple, Dict
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects, repositories, exceptions, models

# ===============
# Payment Verify service
# =======================
class PaymentVerifyService:
    def __init__(self, payment_gateway_repository: repositories.PaymentGatewayRepository):
        self.payment_gateway_repository = payment_gateway_repository
    
    def verify_payment(self, order: models.Order, transaction_id: str):
        payment_details = self.payment_gateway_repository.get_payment_details(transaction_id)

        if payment_details.order_id != order.order_id:
            return False, None
            #TODO log
            #raise exceptions.InvalidPaymentOperation("Payment Verification Order ID mismatch")

        if payment_details.paid_amount != order.final_amount:
            return False, None
            #TODO log
            #raise exceptions.InvalidPaymentOperation(f"Transaction Amount mismatch: expected {order.final_amount.amount} {order.final_amount.currency}")

        if payment_details.status != "COMPLETED":
            return False, None
            #TODO log
            #raise exceptions.InvalidPaymentOperation("Transaction not completed")
        
        return True, payment_details