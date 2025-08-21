from __future__ import annotations
from typing import List, Dict, Tuple, Type

from ddd.order_management.domain import (
    enums,
    value_objects,
    exceptions,
    services
)

SHIPPING_OPTIONS = List[Type[services.shipping_option_strategies.ShippingOptionStrategyAbstract]]


class ShippingOptionStrategyService:

    def get_applicable_shipping_options(
                self, 
                order: models.Order, 
                vendor_shipping_options: List[value_objects.ShippingOptionStrategy]
            ) -> List[value_objects.ShippingDetails]:

        valid_shipping_options = []

        # check if theres a handler
        for option in vendor_shipping_options:
            for strategy_cls in SHIPPING_OPTIONS:
                if (strategy_cls(option).method == option.method and
                    strategy_cls(option).option_name == option.option_name
                    ):
                    valid_shipping_options.append(
                        strategy_cls(option)
                    )

        # calculate cost if available
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

