from __future__ import annotations
import requests
from decimal import Decimal
from django.conf import settings
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.application import ports

class PaypalPaymentGateway(ports.PaymentGatewayAbstract):

    def __init__(self):
        self.PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
        self.PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
        self.PAYPAL_BASE_URL = "https://api.sandbox.paypal.com"

    def get_payment_details(self, transaction_id: str, order: models.Order) -> value_objects.PaymentDetails:
        url = f"{self.PAYPAL_BASE_URL}/v1/checkout/orders/{transaction_id}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}

        response = requests.get(url, headers=headers)

        return self._map_to_domain(response.json(), order)
    
    def _get_access_token(self):
        self.client_id = self.PAYPAL_CLIENT_ID
        self.client_secret = self.PAYPAL_CLIENT_SECRET
        self.base_url = self.PAYPAL_BASE_URL
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))

        #response.raise_for_status()
        return response.json()["access_token"]

    def _map_to_domain(self, paypal_response, order: models.Order):

        purchase_units = paypal_response.get("purchase_units")

        #TODO need to loop thru?
        paypal_paid_amount = value_objects.Money(
            #amount=sum(Decimal(purchase_unit["amount"]["total"]) for purchase_unit in purchase_units),
            amount=Decimal(purchase_units[0]["amount"]["total"]),
            currency=purchase_units[0]["amount"]["currency"]
        )

        if purchase_units[0].get("custom") != order.order_id:
            raise exceptions.InvalidOrderOperation("Payment Verification Order ID mismatch")

        if paypal_paid_amount != order.final_amount:
            raise exceptions.InvalidOrderOperation(f"Transaction Amount mismatch: expected {order.final_amount.amount} {order.final_amount.currency}")

        if paypal_response.get("status") != "COMPLETED":
            raise exceptions.InvalidOrderOperation("Transaction not completed")


        return value_objects.PaymentDetails(
            method=enums.PaymentMethod.PAYPAL,
            paid_amount=paypal_paid_amount,
            transaction_id=paypal_response.get("id"),
            order_id=purchase_units[0].get("custom"),
            status=enums.PaymentStatus.PAID
        )

class StripePaymentGateway(ports.PaymentGatewayAbstract):

    def __init__(self):
        self.STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
        self.STRIPE_BASE_URL = ""

    def get_payment_details(self, transaction_id: str):
        return self._retrieve_payment_intent(transaction_id=transaction_id)
    
    def _retrieve_payment_intent(self, transaction_id):
        self.api_key = self.STRIPE_API_KEY
        self.base_url = self.STRIPE_BASE_URL
        #self.base_url = "https://api.stripe.com/v1"
        url = f"{self.base_url}/payment_intents/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return self._map_to_domain(response.json(), transaction_id)

    def _map_to_domain(self, stripe_response, transaction_id):

        payment_intent = stripe_response

        stripe_paid_amount = value_objects.Money(
            amount=Decimal(payment_intent["amount"] / 100),
            currency=payment_intent["currency"].upper()
        ) 

        stripe_payment_status = "COMPLETED" if payment_intent.get("status") == "succeeded" else None
        stripe_order_id = "ORD-232" #TODO


        return value_objects.PaymentDetails(
            method=enums.PaymentMethod.STRIPE,
            paid_amount=stripe_paid_amount,
            transaction_id=transaction_id,
            order_id=stripe_order_id,
            status=stripe_payment_status
        )

    
class PaymentService(ports.PaymentServiceAbstract):

    def get_payment_gateway(self, payment_method: enums.PaymentMethod) -> ports.PaymentGatewayAbstract:
        gateways = {
            enums.PaymentMethod.PAYPAL: PaypalPaymentGateway(),
            enums.PaymentMethod.STRIPE: StripePaymentGateway()
        }
        if payment_method not in gateways:
            raise ValueError(f"Unsupport payment gateway {payment_method}")

        return gateways[payment_method]