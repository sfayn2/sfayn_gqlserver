from __future__ import annotations
import requests, os
from decimal import Decimal
from django.conf import settings
from ddd.order_management.domain import value_objects, enums, exceptions
from ddd.order_management.application import ports, dtos

PAYPAL_TO_DOMAIN_STATUS = {
    "CREATED": enums.PaymentStatus.PENDING,
    "APPROVED": enums.PaymentStatus.PENDING,
    "COMPLETED": enums.PaymentStatus.PAID,
    "VOIDED": enums.PaymentStatus.CANCELLED,
    "CANCELLED": enums.PaymentStatus.CANCELLED,
}

class PaypalPaymentGateway(ports.PaymentGatewayAbstract):

    def __init__(self, client_id: str, client_secret: str, client_url: str):
        self.paypal_client_id = client_id
        self.paypal_client_secret = client_secret
        self.paypal_base_url = client_url

    def is_eligible(self, order: models.Order) -> bool:
        return True

    def get_payment_details(self, transaction_id: str, order: models.Order) -> value_objects.PaymentDetails:
        url = f"{self.paypal_base_url}/v1/checkout/orders/{transaction_id}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        paypal_response = response.json()

        if paypal_response.get("status") == "COMPLETED":
            self._verify_captures(transaction_id, headers)

        return self._map_to_domain(paypal_response)
    
    def _get_access_token(self):
        url = f"{self.paypal_base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.paypal_client_id, self.paypal_client_secret))

        #response.raise_for_status()
        return response.json()["access_token"]

    def _map_to_domain(self, paypal_response: dict):

        purchase_units = paypal_response.get("purchase_units", [])

        paypal_paid_amount = value_objects.Money(
            amount=sum(Decimal(purchase_unit.get("amount", {}).get("total", "0")) for purchase_unit in purchase_units),
            currency=purchase_units[0].get("amount", {}).get("currency", "USD") if purchase_units else "USD"
        )

        status = PAYPAL_TO_DOMAIN_STATUS.get(paypal_response.get("status"), enums.PaymentStatus.UNKNOWN)
        order_id = purchase_units[0].get("custom") if purchase_units else None

        return value_objects.PaymentDetails(
            method=enums.PaymentMethod.DIGITAL_WALLET,
            paid_amount=paypal_paid_amount,
            transaction_id=paypal_response.get("id"),
            order_id=order_id,
            status=status
        )

    def _verify_captures(self, transaction_id: str, headers: dict) -> None:
        # ensure that at least one capture exists and completed
        capture_url = f"{self.paypal_base_url}/v2/checkout/orders/{transaction_id}/captures"
        response = requests.get(capture_url, headers=headers)
        response.raise_for_status()
        captures = response.json().get("captures", [])

        if not captures:
            raise exceptions.PaymentNotSettledException(f"No capture found for PayPal transaction {transaction_id}")

        completed = any(capture.get("status") == "COMPLETED" for capture in captures)
        if not completed:
            raise exceptions.PaymentNotSettledException(f"PayPal transaction {transaction_id} not fully captured.")
