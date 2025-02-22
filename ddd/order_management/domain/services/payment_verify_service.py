import requests
from decimal import Decimal
from typing import Tuple, Dict
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects, repositories, exceptions

# ==================
# Payment verifier contract
# ======================
class PaymentVerifyStrategy(ABC):
    @abstractmethod
    def verify_payment(self, payment_details: Dict, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
        """
            Verifies the paymen status for a given transaction ID.
            Returns a dictionary containing status and message
        """
    
class PayPalPaymentVerifyStrategy(PaymentVerifyStrategy):

    def verify_payment(self, payment_details: Dict, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
            
        purchase_units = payment_details.get("purchase_units")
        # =====
        # custom_id is internal order_id
        # =====
        if purchase_units.get("custom_id") != order_id:
            return False, "Order ID mismatch"

        actual_amount = value_objects.Money(
            amount=Decimal(purchase_units[0]["amount"]["value"]),
            currency=purchase_units[0]["amount"]["currency_code"]
        ) 
        for purchase_unit in purchase_units[1:]:
            actual_amount = actual_amount.add(
                value_objects.Money(
                    amount=Decimal(purchase_unit["amount"]["value"]),
                    currency=purchase_unit["amount"]["currency_code"]
                )
            )

        if actual_amount != expected_amount:
            return False, f"Transaction Amount mismatch: expected {expected_amount.amount} {expected_amount.currency}"

        if payment_details.get("status") != "COMPLETED":
            return False, "Transaction not completed"
        

        return True, "Payment verified successfully"

class StripePaymentVerifyStrategy(PaymentVerifyStrategy):
    # ========
    # Not tested
    # ==========

    def verify_payment(self, payment_details: Dict, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
        payment_intent = payment_details
        if payment_intent["status"] != "succeeded":
            return False, "Payment verification failed"

        actual_amount = value_objects.Money(
            amount=Decimal(payment_intent["amount"] / 100),
            currency=payment_intent["currency"].upper()
        ) 

        #actual_amount = float(payment_intent["amount"]) / 100 #strip amount are in cents??
        if actual_amount != expected_amount:
            return False, f"Amount mismatch: expected {expected_amount}"
        
        return True, "Payment verified successfully"

# ====================
# Payment Verify Strategy Mapper
# ===========
PAYMENT_STRATEGY = {
    enums.PaymentMethod.PAYPAL: PayPalPaymentVerifyStrategy,
    enums.PaymentMethod.STRIPE: StripePaymentVerifyStrategy
}

# ===============
# Payment Verify service
# =======================
class PaymentVerifyService:
    def __init__(self, payment_gateway_repository: repositories.PaymentGatewayRepository, payment_method: enums.PaymentMethod):
        self.payment_gateway_repository = payment_gateway_repository
        self.payment_method = payment_method
    
    def verify_payment(self, expected_amount: value_objects.Money, transaction_id: str, order_id: str):
        #payment_details = self.payment_gateway_repository.get_payment_details("9S819517D88141438")
        payment_details = self.payment_gateway_repository.get_payment_details(transaction_id)
        strategy_class = PAYMENT_STRATEGY.get(self.payment_method, None)
        if not strategy_class:
            raise ValueError(f"Unsupported Payment Verification: {self.payment_method.value}")

        return strategy_class().verify_payment(
            payment_details=payment_details,
            expected_amount=expected_amount,
            order_id=order_id
            #order_id="9S819517D88141438"
        )
