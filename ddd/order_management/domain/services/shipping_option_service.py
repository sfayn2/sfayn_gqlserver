from __future__ import annotations
import json, pytz
from dataclasses import asdict
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class ShippingOptionStrategy(ABC):

    def __init__(self, strategy: value_objects.ShippingOptionStrategy):
        self.strategy = strategy

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if shipping option is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_current_time(self):
        return datetime.now(pytz.utc).time()

class StandardShippingStrategy(ShippingOptionStrategy):

    def is_eligible(self, order: models.Order) -> bool:
        """
            Only allow packages under 30kg + Domestic shipping
        """
        return order.total_weight <= self.strategy.conditions.get("min_package_weight") and not order.destination.is_international(order.vendor_country)

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Base cost + flat rate per kg
        """
        return self.strategy.base_cost.add(self.strategy.flat_rate.multiply(order.total_weight))

class ExpressShippingStrategy(ShippingOptionStrategy):

    def is_before_cutoff(self):
        return self.get_current_time() <= self.strategy.conditions.get("cutoff_time")

    def is_eligible(self, order: models.Order) -> bool:
        return order.total_weight <= self.strategy.conditions.get("max_weight") and self.is_before_cutoff()

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        return self.strategy.base_cost.add(self.strategy.flat_rate.multiply(order.total_weight))

class LocalPickupShippingStrategy(ShippingOptionStrategy):

    def is_near_by(self, order: models.Order):
        return (order.destination.city in self.strategy.conditions.get("near_by_cities") and 
                order.destination.country == order.vendor_country
        )

    def is_eligible(self, order: models.Order) -> bool:
        current_time = self.get_current_time()
        return (current_time >= self.strategy.conditions.get("pickup_time_from") and 
                current_time <= self.strategy.conditions.get("pickup_time_to") and
                self.is_near_by(order)
        )

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        #default is zero
        return value_objects.Money.default()

class FreeShippingStrategy(ShippingOptionStrategy):

    def is_eligible(self, order: models.Order) -> bool:
        #orders above $50?
        return order.sub_total > self.strategy.conditions.get("min_order_amount")

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        #default is zero
        return value_objects.Money.default()


# ==============
# Shipping Option Strategy Mapper
# ===============

# when adding new options strategy need to map the strategy
SHIPPING_OPTIONS_STRATEGIES = {
    enums.ShippingMethod.STANDARD: StandardShippingStrategy,
    enums.ShippingMethod.EXPRESS: ExpressShippingStrategy,
    enums.ShippingMethod.LOCAL_PICKUP: LocalPickupShippingStrategy,
    enums.ShippingMethod.FREE_SHIPPING: FreeShippingStrategy
}


class ShippingOptionStrategyService:

    def __init__(self, vendor_repository: repositories.VendorRepository):
        self.vendor_repository = vendor_repository

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
            ship_opt_strategy_class = SHIPPING_OPTIONS_STRATEGIES.get(option.name)
            valid_shipping_options.append(
                ship_opt_strategy_class(option)
            )

        return valid_shipping_options
