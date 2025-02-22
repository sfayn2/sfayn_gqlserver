import requests
from ddd.order_management.domain import repositories
from django.conf import settings

class PaypalPaymentGatewayRepository(repositories.PaymentGatewayRepository):

    def get_payment_details(self, order_id: str):
        url = f"{settings.PAYPAL_BASE_URL}/v1/checkout/orders/{order_id}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}

        response = requests.get(url, headers=headers)
        #response.raise_for_status()

        return response.json()
    
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
    