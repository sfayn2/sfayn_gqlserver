from __future__ import annotations
import requests
from typing import List, Type
from decimal import Decimal
from ddd.order_management.domain import value_objects, enums, exceptions
from ddd.order_management.application import ports


class PaymentService:

    def __init__(self, payment_options: List[ports.PaymentGatewayAbstract]):
        self.payment_options = payment_options

    def select_payment_option(self, 
        payment_method: enums.PaymentMethod, 
        provider: str,
        vendor_payment_options: List[dtos.VendorPaymentOptionSnapshotDTO]
    ) -> ports.PaymentGatewayAbstract:

        valid_payment_options = []

        # payment options to handler 
        for vendor_option in vendor_payment_options: #source alwys assumed its active
            key = (payment_method, provider.lower())
            strategy_factories = self.payment_options.get(key, [])
            for factory in strategy_factories:
                # expected to have a single payment option per method + provder
                return factory(vendor_option.tenant_id)

        raise exceptions.SelectPaymentOptionException(f"Unsupport payment option {payment_method} {provider}")
