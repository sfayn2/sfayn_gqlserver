import requests
from typing import Tuple
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects, repositories, exceptions

# ==================
# Payment verifier contract
# ======================
class PaymentVerifierStrategy(ABC):
    @abstractmethod
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
        """
            Verifies the paymen status for a given transaction ID.
            Returns a dictionary containing status and message
        """
    
class PayPalPaymentVerifierStrategy(PaymentVerifierStrategy):
    def __init__(self, paypal_gateway_repository: repositories.PaymentGatewayRepository):
        self.paypal_gateway_repository = paypal_gateway_repository

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
        try:
            transaction = self.paypal_gateway_repository.get_payment_details(transaction_id)
            
            if transaction["supplementary_data"]["related_ids"]["order_id"] != order_id:
                return False, "Order ID mismatch"

            actual_amount = value_objects.Money(
                amount=transaction["amount"]["value"],
                currency=transaction["amount"]["currency_code"]
            ) 

            if actual_amount != expected_amount:
                return False, f"Transaction Amount mismatch: expected {expected_amount}"

            if transaction["status"] != "COMPLETED":
                return False, "Transaction not completed"
            

            return True, "Payment verified successfully"
        except Exception as e:
            return False, str(e)

class StripePaymentVerifierStrategy(PaymentVerifierStrategy):
    def __init__(self, stripe_gateway_repository: repositories.PaymentGatewayRepository):
        self.stripe_gateway_repository = stripe_gateway_repository

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money, order_id: str) -> Tuple[bool, str]:
        payment_intent = self.stripe_gateway_repository.get_payment_details(transaction_id)
        if payment_intent["status"] != "succeeded":
            return False, "Payment verification failed"

        actual_amount = value_objects.Money(
            amount=payment_intent["amount"] / 100,
            currency=payment_intent["currency"].upper()
        ) 

        #actual_amount = float(payment_intent["amount"]) / 100 #strip amount are in cents??
        if actual_amount != expected_amount:
            return False, f"Amount mismatch: expected {expected_amount}"
        
        return True, "Payment verified successfully"

# ====================
# Payment Verifier Strategy Mapper
# ===========
PAYMENT_STRATEGY = {
    enums.PaymentMethod.PAYPAL: PayPalPaymentVerifierStrategy,
    enums.PaymentMethod.STRIPE: StripePaymentVerifierStrategy
}

# ===============
# Payment Verifier service
# =======================
class PaymentService:
    def __init__(self, payment_gateway_repository: repositories.PaymentGatewayRepository, payment_method: enums.PaymentMethod):
        self.payment_gateway_repository = payment_gateway_repository
        self.payment_method = payment_method
    
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money, order_id: str):
        strategy_class = PAYMENT_STRATEGY.get(self.payment_method, None)
        if not strategy_class:
            raise ValueError(f"Unsupported payment method: {self.payment_method.value}")

        return strategy_class(self.payment_gateway_repository).verify_payment(
            transaction_id=transaction_id,
            expected_amount=expected_amount,
            order_id=order_id
        )
