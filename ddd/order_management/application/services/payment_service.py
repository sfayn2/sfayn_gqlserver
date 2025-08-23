from __future__ import annotations
import requests
from typing import List, Type
from decimal import Decimal
from ddd.order_management.domain import value_objects, enums, exceptions
from ddd.order_management.application import ports


class PaymentService:

    def __init__(self, payment_options: List[ports.PaymentGatewayAbstract]):
        self.payment_options = payment_options

    def select_payment_option(
        self, 
        method: enums.PaymentMethod, 
        provider: str,
        vendor_payment_options: List[dtos.VendorPaymentOptionSnapshotDTO]
    ) -> ports.PaymentGatewayAbstract:

        for vendor_option in vendor_payment_options:
            if vendor_option.method == method and vendor_option.provider == provider:
                return vendor_option


    def get_applicable_payment_options(
        self,
        order: models.Order, 
        vendor_payment_options: List[dtos.VendorPaymentOptionSnapshotDTO]
    ) -> List[dtos.PaymentOptionDTO]:

        valid_payment_options = []

        # check if payment option have available handler
        for vendor_option in vendor_payment_options:
            key = (payment_method, provider.lower())
            strategy_factories = self.payment_options.get(key, [])
            for factory in strategy_factories:
                payment_ins =  factory(vendor_option.tenant_id)
                valid_payment_options(payment_ins)

        options = []
        for option in valid_payment_options:
            if option.is_eligible(order):
                options.append(dtos.PaymentOptionDTO(
                        option_name=option.option_name,
                        method=option.method,
                        provider=option.provider)
                )

        if not options:
            raise exceptions.NoApplicablePaymentOptionException(f"No available payment options.")

        return options

    def resolve_payment_option(
        self,
        payment_method: enums.PaymentMethod,
        provider: str,
        vendor_payment_options: List[dtos.PaymentOptionDTO],
        order: models.Order,
        transaction_id: str
    ) -> value_objects.PaymentDetails:

        available_payment_options = self.get_applicable_payment_options(
            order=order,
            vendor_payment_options=vendor_payment_options
        )

        payment_option = self.select_payment_option(
            payment_method, 
            provider,
            available_payment_options
        )

        return payment_option.get_payment_details(
            command.transaction_id,
            order=order
        )