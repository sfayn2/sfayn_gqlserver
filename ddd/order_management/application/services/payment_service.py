from __future__ import annotations
import requests
from decimal import Decimal
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.application import ports

PAYMENT_GATEWAYS: Dict[enums.PaymentMethod, ports.PaymentGatewayAbstract] = {}

    
class PaymentService:

    #def __init__(self, payment_gateways: Dict[enums.PaymentMethod, ports.PaymentGatewayAbstract]):
    #    self.payment_gateways = payment_gateways

    def get_payment_gateway(self, payment_method: enums.PaymentMethod) -> ports.PaymentGatewayAbstract:
        if payment_method not in PAYMENT_GATEWAYS:
            raise ValueError(f"Unsupport payment gateway {payment_method}")

        return PAYMENT_GATEWAYS.get(payment_method)