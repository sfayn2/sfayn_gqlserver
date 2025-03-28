from __future__ import annotations
import json, pytz
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class ShippingOptionStrategy(value_objects.ShippingOptionStrategy):

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

class StandardShippingStrategy(ShippingOptionStrategy):

    def is_eligible(self, order: models.Order) -> bool:
        """
            Only allow packages under 30kg + Domestic shipping
        """
        return order.total_weight <= self.conditions.get("total_weight") and not order.destination.is_international(order.vendor_country)

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Base cost + flat rate per kg
        """
        currency = order.currency
        return value_objects.Money(
            amount=self.base_cost + (self.flat_rate * order.total_weight),
            currency=currency
        )

class ExpressShippingStrategy(ShippingOptionStrategy):

    def is_before_cutoff(self):
        current_time = datetime.now(pytz.utc).time()
        return current_time <= self.conditions.get("cutoff_time")

    def is_eligible(self, order: models.Order) -> bool:
        return order.total_weight <= self.conditions.get("total_weight") and self.is_before_cutoff()

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        currency = order.currency
        return value_objects.Money(
            amount=self.base_cost + (self.flat_rate * order.total_weight),
            currency=currency
        )

class LocalPickupShippingStrategy(ShippingOptionStrategy):

    #def is_near_by(self):
    #    pass

    def is_eligible(self, order: models.Order) -> bool:
        #TODO nearby only?
        current_time = datetime.now(pytz.utc).time()
        return current_time >= self.conditions.get("pickup_hours_from") and current_time <= self.conditions.get("pickup_hours_to")

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        #default is zero
        return value_objects.Money.default()

class FreeShippingStrategy(ShippingOptionStrategy):

    def is_eligible(self, order: models.Order) -> bool:
        #orders above $50?
        return order.sub_total > self.conditions.get("total_orders")

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


class ShippingMethodStrategyService:

    def __init__(self, vendor_repository: repositories.VendorRepository):
        self.vendor_repository = vendor_repository

    def get_shipping_options(self, order: models.Order) -> List[dict]:
        options = []
        for option in self._fetch_valid_options():
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append({
                    "name": option.name,
                    "delivery_time": option.delivery_time,
                    "cost": cost
                })
        return options

    def _fetch_valid_options(self, vendor_name: str):
        vendor_shipping_options = self.vendor_repository.get_shipping_options(vendor_name)
        valid_shipping_options = []

        for option in vendor_shipping_options:
            ship_opt_strategy_class = SHIPPING_OPTIONS_STRATEGIES.get(option.name)
            valid_shipping_options.append(
                ship_opt_strategy_class(
                    name=option.name,
                    delivery_time=option.delivery_time,
                    conditions=option.conditions,
                    base_cost=option.base_cost,
                    flat_rate=option.flat_rate
                )
            )

        return valid_shipping_options

        #self.shipping_options = [
        #    shipping_option_service.ShippingMethodStrategy(
        #        name=enums.ShippingMethod.STANDARD,
        #        delivery_time="3-5 business days",
        #        base_cost=Decimal("5.00")
        #    ),
        #    shipping_option_service.ShippingMethodStrategy(
        #        name=enums.ShippingMethod.EXPRESS,
        #        delivery_time="1-2 business days",
        #        base_cost=Decimal("15.00")
        #    ),
        #    shipping_option_service.ShippingMethodStrategy(
        #        name=enums.ShippingMethod.SAME_DAY,
        #        delivery_time="same day",
        #        base_cost=Decimal("25.00")
        #    ),
        #    shipping_option_service.ShippingMethodStrategy(
        #        name=enums.ShippingMethod.FLAT_RATE,
        #        delivery_time="4-6 business days",
        #        base_cost=Decimal("10.00"),
        #        flat_rate=Decimal("2.00")
        #    )