import requests
from ddd.order_management.domain import repositories
from django.conf import settings

class PaypalPaymentGatewayRepository(repositories.PaymentGatewayRepository):
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = settings.PAYPAL_BASE_URL
        #self.base_url = "https://api-m.sandbox.paypal.com"
        self.access_token = self._get_access_token()

    def get_payment_details(self, transaction_id: str):
        url = f"{self.base_url}/v1/reporting/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)
        response.raise_to_status()

        return response.json()
    
    def _get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))

        response.raise_for_status()
        return response.json()["access_token"]
    