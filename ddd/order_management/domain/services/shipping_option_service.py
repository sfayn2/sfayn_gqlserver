from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class ShippingOptionStrategy(ABC):
    def __init__(self, name: enums.ShippingMethod, delivery_time: str, base_cost: Decimal, flat_rate: Decimal, conditions: dict):
        self.name = name
        self.delivery_time = delivery_time
        self.conditions = conditions
        self.base_cost = base_cost
        self.flat_rate = flat_rate

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if shipping option is eligible for the given package.
        """
        return True

    @abstractmethod
    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        currency = order.currency
        return value_objects.Money(
            amount=self.base_cost,
            currency=currency
        )

class ShippingOption1Strategy(ShippingOptionStrategy):

    def is_eligible(self, order: models.Order) -> bool:
        """
            Only allow packages under 30kg
        """
        return order.total_weight <= Decimal(30)

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Base cost + flat rate per kg
        """
        currency = order.currency
        return value_objects.Money(
            amount=self.base_cost + (self.flat_rate * order.total_weight),
            currency=currency
        )


class ShippingOptionStrategyService:

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
            valid_shipping_options.append(
                ShippingOptionStrategy(
                    name=option.get("name"),
                    delivery_time=option.get("delivery_time"),
                    conditions=json.loads(option.get("conditions")),
                    base_cost=option.get("base_cost"),
                    flat_rate=option.get("flat_rate")
                )
            )

        return valid_shipping_options

        #self.shipping_options = [
        #    shipping_option_service.ShippingOptionStrategy(
        #        name=enums.ShippingMethod.STANDARD,
        #        delivery_time="3-5 business days",
        #        base_cost=Decimal("5.00")
        #    ),
        #    shipping_option_service.ShippingOptionStrategy(
        #        name=enums.ShippingMethod.EXPRESS,
        #        delivery_time="1-2 business days",
        #        base_cost=Decimal("15.00")
        #    ),
        #    shipping_option_service.ShippingOptionStrategy(
        #        name=enums.ShippingMethod.SAME_DAY,
        #        delivery_time="same day",
        #        base_cost=Decimal("25.00")
        #    ),
        #    shipping_option_service.ShippingOptionStrategy(
        #        name=enums.ShippingMethod.FLAT_RATE,
        #        delivery_time="4-6 business days",
        #        base_cost=Decimal("10.00"),
        #        flat_rate=Decimal("2.00")
        #    )