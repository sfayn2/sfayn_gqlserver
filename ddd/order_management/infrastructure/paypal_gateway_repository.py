import requests
from decimal import Decimal
from ddd.order_management.domain import repositories, value_objects, enums
from ddd.order_management.infrastructure import order_dtos
from django.conf import settings

class PaypalPaymentGatewayRepository(repositories.PaymentGatewayRepository):

    def get_payment_details(self, transaction_id: str) -> value_objects.PaymentDetails:
        url = f"{settings.PAYPAL_BASE_URL}/v1/checkout/orders/{transaction_id}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}

        response = requests.get(url, headers=headers)

        return self._map_to_domain(response.json())
    
    def _get_access_token(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = settings.PAYPAL_BASE_URL
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))

        #response.raise_for_status()
        return response.json()["access_token"]

    def _map_to_domain(self, paypal_response):

        purchase_units = paypal_response.get("purchase_units")

        #TODO need to loop thru?
        paypal_paid_amount = order_dtos.MoneyDTO(
            #amount=sum(Decimal(purchase_unit["amount"]["total"]) for purchase_unit in purchase_units),
            amount=Decimal(purchase_units[0]["amount"]["total"]),
            currency=purchase_units[0]["amount"]["currency"]
        )

        return order_dtos.PaymentDetailsDTO(
            method=enums.PaymentMethod.PAYPAL,
            paid_amount=paypal_paid_amount,
            transaction_id=paypal_response.get("id"),
            order_id=purchase_units[0].get("custom"),
            status=paypal_response.get("status")
        ).to_domain()
