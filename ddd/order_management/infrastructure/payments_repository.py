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

class StripePaymentGatewayRepository(repositories.PaymentGatewayRepository):

    def get_payment_details(self, transaction_id: str):
        return self._retrieve_payment_intent(transaction_id=transaction_id)
    
    def _retrieve_payment_intent(self, transaction_id):
        self.api_key = settings.STRIPE_API_KEY
        self.base_url = settings.STRIPE_BASE_URL
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


        return order_dtos.PaymentDetailsDTO(
            method=enums.PaymentMethod.STRIPE,
            paid_amount=stripe_paid_amount,
            transaction_id=transaction_id,
            order_id=stripe_order_id,
            status=stripe_payment_status
        ).to_domain()

    

class PaymentGatewayFactory:

    @staticmethod
    def get_payment_gateway(payment_method: enums.PaymentMethod):
        gateways = {
            enums.PaymentMethod.PAYPAL: PaypalPaymentGatewayRepository(),
            enums.PaymentMethod.STRIPE: StripePaymentGatewayRepository()
        }
        if payment_method not in gateways:
            raise ValueError(f"Unsupport payment gateway {payment_method}")

        return gateways[payment_method]
