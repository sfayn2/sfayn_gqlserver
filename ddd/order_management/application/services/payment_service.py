from __future__ import annotations
import requests
from typing import List, Type
from decimal import Decimal
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.application import ports


class PaymentService:

    def __init__(self, payment_options: List[ports.PaymentGatewayAbstract]):
        self.payment_options = payment_options

    def select_payment_option(self, payment_method: enums.PaymentMethod, provider: str) -> ports.PaymentGatewayAbstract:

        for option in payment_options:
            if (payment_method == option.payment_option.method and 
            provider == option.payment_option.provider):
                return option

        raise ValueError(f"Unsupport payment option {payment_method} {provider}")
