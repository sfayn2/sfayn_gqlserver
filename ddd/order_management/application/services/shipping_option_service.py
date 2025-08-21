from __future__ import annotations
from typing import List, Dict, Tuple

from ddd.order_management.domain import (
    enums,
    value_objects,
    exceptions,
    services
)

SHIPPING_OPTIONS = Tuple[Tuple[enums.ShippingMethod, services.shipping_option_strategies.ShippingOptionStrategyAbstract]]


class ShippingOptionStrategyService:

    def get_applicable_shipping_options(
                self, 
                order: models.Order, 
                vendor_shipping_options: List[value_objects.ShippingOptionStrategy]
            ) -> List[value_objects.ShippingDetails]:

        valid_shipping_options = []

        for option in vendor_shipping_options:
            for so in SHIPPING_OPTIONS:
                if option.option_name == so[0]:
                    valid_shipping_options.append(
                        ship_opt_strategy_class(option)
                    )

        options = []
        for option in valid_shipping_options:
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append(value_objects.ShippingDetails(
                        method=option.option_name,
                        delivery_time=option.delivery_time,
                        cost=cost)
                )

        if not options:
            raise exceptions.InvalidOrderOperation(f"No available shipping options.")

        return options

