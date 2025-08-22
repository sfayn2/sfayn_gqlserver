from __future__ import annotations
import requests, os
from decimal import Decimal
from django.conf import settings
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.application import ports, dtos


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

    @property
    def payment_option(self):
        return {
            "method": enums.PaymentMethod.DIGITAL_WALLET,
            "provider": "paypal"
        }

    