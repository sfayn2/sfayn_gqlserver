import requests
from typing import Tuple
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects, repositories

class PaymentVerifierStrategy(ABC):
    @abstractmethod
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        """
            Verifies the paymen status for a given transaction ID.
            Returns a dictionary containing status and message
        """
    
class PayPalPaymentVerifierStrategy(PaymentVerifierStrategy):
    def __init__(self, paypal_gateway_repository: repositories.PaymentGatewayRepository):
        self.paypal_gateway_repository = paypal_gateway_repository

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        try:
            transaction = self.paypal_gateway_repository.get_payment_details(transaction_id)
            if transaction["transaction_status"] != "S":
                return False, "Payment verification failed"

            actual_amount = value_objects.Money(
                amount=transaction["transaction_amount"]["value"],
                currency=transaction["transaction_amount"]["currency_code"]
            ) 

            if actual_amount != expected_amount:
                return False, f"Amount mismatch: expected {expected_amount}"

            return True, "Payment verified successfully"
        except Exception as e:
            return False, str(e)

class StripePaymentVerifierStrategy(PaymentVerifierStrategy):
    def __init__(self, stripe_gateway_repository: repositories.PaymentGatewayRepository):
        self.stripe_gateway_repository = stripe_gateway_repository

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
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
    
class CashOnDeliveryPaymentVerifierStrategy(PaymentVerifierStrategy):
    def __init__(self, cod_gateway_repository: repositories.PaymentGatewayRepository):
        self.cod_gateway_repository = cod_gateway_repository

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        #TODO? N/A?
        print(f"Verifying Cash on Delivery for transaction {transaction_id}")
        return True, "Payment verified successfully"


class PaymentService:
    def __init__(self, payment_gateway_repository: repositories.PaymentGatewayRepository, payment_method: enums.PaymentMethod):
        self.payment_gateway_repository = payment_gateway_repository
        self.payment_method = payment_method
    
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money):
        if self.payment_method == enums.PaymentMethod.PAYPAL:
            strategy = PayPalPaymentVerifierStrategy(
                paypal_gateway_repository=self.payment_gateway_repository
            )
        elif self.payment_method == enums.PaymentMethod.STRIPE:
            strategy = StripePaymentVerifierStrategy(
                stripe_gateway_repository=self.payment_gateway_repository
            )
        elif self.payment_method == enums.PaymentMethod.COD:
            strategy = CashOnDeliveryPaymentVerifierStrategy(
                cod_gateway_repository=self.cod_gateway_repository
            )
        else:
            raise ValueError(f"Unsupported payment method: {self.payment_method.value}")

        return strategy.verify_payment(
            transaction_id=transaction_id,
            expected_amount=expected_amount
        )