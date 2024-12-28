import requests
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums, value_objects

class PaymentVerifierPolicy(ABC):
    @abstractmethod
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money) -> dict:
        """
            Verifies the paymen status for a given transaction ID.
            Returns a dictionary containing status and message
        """
    
class PayPalPaymentVerifierPolicy(PaymentVerifierPolicy):
    def __init__(self, paypal_client):
        self.paypal_client = paypal_client

    def verify_payment(self, transaction_id, expected_amount: value_objects.Money):
        try:
            transaction = self.paypal_client.search_transaction(transaction_id)
            if transaction["transaction_status"] != "S":
                return {"status": "failed", "message": "Payment verification failed"}

            actual_amount = value_objects.Money(
                _amount=transaction["transaction_amount"]["value"],
                _currency=transaction["transaction_amount"]["currency_code"]
            ) 

            if actual_amount != expected_amount:
                return {"status": "failed", "message": f"Amount mismatch: expected {expected_amount}"}

            return {"status": "succeeded", "message": "Payment verified successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class StripePaymentVerifierPolicy(PaymentVerifierPolicy):
    def __init__(self, stripe_client):
        self.stripe_client = stripe_client

    def verify_payment(self, transaction_id, expected_amount: value_objects.Money):
        payment_intent = self.stripe_client.retrieve_payment_intent(transaction_id)
        if payment_intent["status"] != "succeeded":
            return {"status": "failed", "message": "Payment verification failed"}

        actual_amount = value_objects.Money(
            _amount=payment_intent["amount"] / 100,
            _currency=payment_intent["currency"].upper()
        ) 

        #actual_amount = float(payment_intent["amount"]) / 100 #strip amount are in cents??
        if actual_amount != expected_amount:
            return {"status": "failed", "message": f"Amount mismatch: expected {expected_amount}"}
        
        return {"status": "succeeded", "message": "Payment verified successfully"}
    
class CashOnDeliveryPaymentVerifierPolicy(PaymentVerifierPolicy):
    def verify_payment(self, transaction_id: str, expected_amount: value_objects.Money):
        #TODO? N/A?
        print(f"Verifying Cash on Delivery for transaction {transaction_id}")
        return {"status": "succeeded", "message": "Payment verified successfully"}



class PaymentVerifierFactory:

    def __init__(self, client: dict):
        self.client = client

    def get_verifier(self, payment_method: enums.PaymentMethod):
        if payment_method == enums.PaymentMethod.PAYPAL:
            return PayPalPaymentVerifierPolicy(
                paypal_client=self.client
            )
        elif payment_method == enums.PaymentMethod.STRIPE:
            return StripePaymentVerifierPolicy(
                stripe_client=self.client
            )
        elif payment_method == enums.PaymentMethod.COD:
            return CashOnDeliveryPaymentVerifierPolicy()
        else:
            raise ValueError(f"Unsupported payment method: {payment_method.value}")