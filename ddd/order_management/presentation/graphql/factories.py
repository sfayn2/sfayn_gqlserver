from ddd.order_management.infrastructure.adapters import payments_adapter
from ddd.order_management.domain import enums

class PaymentGatewayFactory:

    @staticmethod
    def get_payment_gateway(payment_method: enums.PaymentMethod):
        gateways = {
            enums.PaymentMethod.PAYPAL: payments_adapter.PaypalPaymentGatewayAdapter(),
            enums.PaymentMethod.STRIPE: payments_adapter.StripePaymentGatewayAdapter()
        }
        if payment_method not in gateways:
            raise ValueError(f"Unsupport payment gateway {payment_method}")

        return gateways[payment_method]