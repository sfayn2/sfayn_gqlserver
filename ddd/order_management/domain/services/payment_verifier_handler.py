import requests
from typing import Tuple
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects

class PaymentVerifierHandler(ABC):
    @abstractmethod
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        """
            Verifies the paymen status for a given transaction ID.
            Returns a dictionary containing status and message
        """
    
class PayPalPaymentVerifierHandler(PaymentVerifierHandler):
    def __init__(self, paypal_client):
        self.paypal_client = paypal_client

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        try:
            transaction = self.paypal_client.search_transaction(transaction_id)
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

class StripePaymentVerifierHandler(PaymentVerifierHandler):
    def __init__(self, stripe_client):
        self.stripe_client = stripe_client

    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        payment_intent = self.stripe_client.retrieve_payment_intent(transaction_id)
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
    
class CashOnDeliveryPaymentVerifierHandler(PaymentVerifierHandler):
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> Tuple[bool, str]:
        #TODO? N/A?
        print(f"Verifying Cash on Delivery for transaction {transaction_id}")
        return True, "Payment verified successfully"


