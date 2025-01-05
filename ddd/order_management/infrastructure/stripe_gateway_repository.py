import requests
from ddd.order_management.domain import repositories
from django.conf import settings

class StripePaymentGatewayRepository(repositories.PaymentGatewayRepository):
    def __init__(self):
        self.api_key = settings.STRIPE_API_KEY
        self.base_url = settings.STRIPE_BASE_URL
        #self.base_url = "https://api.stripe.com/v1"

    def get_payment_details(self, transaction_id: str):
        return self._retrieve_payment_intent(transaction_id=transaction_id)
    
    def _retrieve_payment_intent(self, transaction_id):
        url = f"{self.base_url}/payment_intents/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
    