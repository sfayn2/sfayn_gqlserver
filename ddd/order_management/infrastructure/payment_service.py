import requests
from ddd.order_management.domain.services import payment_verifier_handler
from ddd.order_management.domain import enums

class StripeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stripe.com/v1"

    def retrieve_payment_intent(self, transaction_id):
        url = f"{self.base_url}/payment_intents/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

class PayPayClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api-m.sandbox.paypal.com"
        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en-US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to get access token {response.text}")
    
    def search_transaction(self, transaction_id):
        url = f"{self.base_url}/v1/reporting/transactions"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "transaction_id": transaction_id,
            "start_date": "2023-12-27T00:00:00",
            "end_date": "2023-12-31T00:00:00"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            transactions = response.json().get("transaction_details", [])
            if transactions:
                return transactions[0]["transaction_info"]
            else:
                raise Exception(f"No transaction found for ID {transaction_id}")
        else:
            raise Exception(f"Failed to search transaction {response.text}")

class PaymentService:
    def __init__(self, client: dict):
        self.client = client
    
    def verify_payment(self, transaction_id: str, payment_method: enums.PaymentMethod):
        if payment_method == enums.PaymentMethod.PAYPAL:
            handler = payment_verifier_handler.PayPalPaymentVerifierHandler(
                paypal_client=self.client
            )
        elif payment_method == enums.PaymentMethod.STRIPE:
            handler = payment_verifier_handler.StripePaymentVerifierHandler(
                stripe_client=self.client
            )
        elif payment_method == enums.PaymentMethod.COD:
            handler = payment_verifier_handler.CashOnDeliveryPaymentVerifierHandler()
        else:
            raise ValueError(f"Unsupported payment method: {payment_method.value}")

        return handler.verify_payment(
            transaction_id=transaction_id,
            payment_method=payment_method
        )