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
        return self._search_transaction(transaction_id=transaction_id)
    
    def _get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to get access token {response.text}")
    
    def _search_transaction(self, transaction_id):
        url = f"{self.base_url}/v1/reporting/transactions"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        #params = {
        #    "transaction_id": transaction_id,
        #    "start_date": "2023-12-27T00:00:00",
        #    "end_date": "2023-12-31T00:00:00"
        #}
        params = {
            "transaction_id": transaction_id
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            transactions = response.json().get("transaction_details", [])
            if transactions:
                return transactions[0]["transaction_info"]
        return []