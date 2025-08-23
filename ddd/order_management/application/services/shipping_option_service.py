from __future__ import annotations
from typing import List, Dict, Tuple, Type

from ddd.order_management.domain import (
    enums,
    value_objects,
    exceptions,
)
from ddd.order_management.application import (
    mappers
)

from ddd.order_management.domain.services import shipping_option_strategies

#SHIPPING_OPTIONS = List[shipping_option_strategies.port.ShippingOptionStrategyAbstract]


class ShippingOptionService:

    def __init__(self, shipping_options: Dict[
        Tuple[enums.ShippingMethod, str], 
        List[shipping_option_strategies.port.ShippingOptionStrategyAbstract]
    ]):
        self.shipping_options = shipping_options

    def get_applicable_shipping_options(
                self, 
                order: models.Order, 
                vendor_shipping_options: List[value_objects.ShippingOptionStrategy]
            ) -> List[value_objects.ShippingDetails]:

        valid_shipping_options = []

        # shipping options to handler 
        for vendor_option in vendor_shipping_options: #source alwys assumed its active
            key = (vendor_option.method, vendor_option.provider.lower())
            strategy_factories = self.shipping_options.get(key, [])
            for factory in strategy_factories:
                strategy_ins = factory(
                    vendor_option.tenant_id, 
                    mappers.ShippingOptionStrategyMapper.to_domain(vendor_option)
                )
                valid_shipping_options.append(strategy_ins)


        # calculate cost if available
        options = []
        for option in valid_shipping_options:
            if option.is_eligible(order):
                options.append(value_objects.ShippingDetails(
                        method=option.option_name,
                        delivery_time=option.delivery_time,
                        cost=option.calculate_cost(order))
                )

        if not options:
            raise exceptions.NoApplicableShippingOptionException(f"No available shipping options.")

        return options

