from __future__ import annotations
import requests, os
from decimal import Decimal
from django.conf import settings
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.application import ports, dtos

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

        return value_objects.PaymentDetails(
            method=enums.PaymentMethod.PAYPAL,
            paid_amount=paypal_paid_amount,
            transaction_id=paypal_response.get("id"),
            order_id=purchase_units[0].get("custom"),
            status=enums.PaymentStatus.PAID
        )

    @property
    def payment_option(self) -> dtos.PaymentOptionDTO:
        return dtos.PaymentOptionDTO(
            method=enums.PaymentMethod.DIGITAL_WALLET,
            provider="paypal"
        )