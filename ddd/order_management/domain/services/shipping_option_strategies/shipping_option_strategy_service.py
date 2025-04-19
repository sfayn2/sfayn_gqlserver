from typing import List, Dict

from ddd.order_management.domain import (
    repositories,
    models,
    enums,
    value_objects
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

    def __init__(self, vendor_repository: repositories.VendorRepository, shipping_options_strategy: SHIPPING_OPTIONS_STRATEGIES = DEFAULT_SHIPPING_OPTIONS_STRATEGIES):
        self.vendor_repository = vendor_repository
        self.shipping_options_strategy = shipping_options_strategy

    def get_shipping_options(self, order: models.Order) -> List[value_objects.ShippingDetails]:
        options = []
        for option in self._fetch_valid_options(vendor_name=order.vendor_name):
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append(value_objects.ShippingDetails(
                        method=option.strategy.name,
                        delivery_time=option.strategy.delivery_time,
                        cost=cost)
                )
        return options

    def _fetch_valid_options(self, vendor_name: str):
        vendor_shipping_options = self.vendor_repository.get_shipping_options(vendor_name=vendor_name)
        valid_shipping_options = []

        for option in vendor_shipping_options:
            ship_opt_strategy_class = self.shipping_options_strategy.get(option.name)
            valid_shipping_options.append(
                ship_opt_strategy_class(option)
            )

        return valid_shipping_options
