import uuid
from typing import List, Dict

from ddd.order_management.domain import (
    repositories,
    models,
    enums,
    value_objects,
    exceptions
    )

from ddd.order_management.domain.services.shipping_option_strategies import (
    standard_shipping,
    express_shipping,
    local_pickup_shipping,
    free_shipping,
    ports
)

# ==============
# Shipping Option Strategy Mapper
# ===============

# when adding new options strategy need to map the strategy
DEFAULT_SHIPPING_OPTIONS_STRATEGIES = {
    enums.ShippingMethod.STANDARD: standard_shipping.StandardShippingStrategy,
    enums.ShippingMethod.EXPRESS: express_shipping.ExpressShippingStrategy,
    enums.ShippingMethod.LOCAL_PICKUP: local_pickup_shipping.LocalPickupShippingStrategy,
    enums.ShippingMethod.FREE_SHIPPING: free_shipping.FreeShippingStrategy
}
SHIPPING_OPTIONS_STRATEGIES = Dict[enums.ShippingMethod, ports.ShippingOptionStrategyAbstract]


class ShippingOptionStrategyService(ports.ShippingOptionStrategyServiceAbstract):

    def __init__(self, shipping_options_strategy: SHIPPING_OPTIONS_STRATEGIES = DEFAULT_SHIPPING_OPTIONS_STRATEGIES):
        self.shipping_options_strategy = shipping_options_strategy

    def get_applicable_shipping_options(
                self, 
                order: models.Order, 
                vendor_shipping_options: List[value_objects.ShippingOptionStrategy]
            ) -> List[value_objects.ShippingDetails]:

        valid_shipping_options = []

        for option in vendor_shipping_options:
            ship_opt_strategy_class = self.shipping_options_strategy.get(option.name)
            valid_shipping_options.append(
                ship_opt_strategy_class(option)
            )

        options = []
        for option in valid_shipping_options:
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append(value_objects.ShippingDetails(
                        method=option.strategy.name,
                        delivery_time=option.strategy.delivery_time,
                        cost=cost)
                )

        if not options:
            raise exceptions.InvalidOrderOperation(f"No available shipping options.")

        return options

