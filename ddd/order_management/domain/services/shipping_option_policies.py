from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects
from decimal import Decimal

class ShippingOption(ABC):
    def __init__(self, name: enums.ShippingMethod, delivery_time: str, base_cost: Decimal):
        self.name = name
        self.delivery_time = delivery_time
        self.base_cost = base_cost

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if shipping option is eligible for the given package.
        """
        return True

    @abstractmethod
    def calculate_cost(self, order: models.Order) -> Decimal:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        return self.base_cost

class Vendor1ShippingOption(ShippingOption):
    def __init__(self, name: str, delivery_time: str, base_cost: Decimal, flat_rate: Decimal):
        super().__init__(name, delivery_time, base_cost)
        self.flat_rate = flat_rate

    def is_eligible(self, order: models.Order) -> bool:
        """
            Only allow packages under 30kg
        """
        return order.get_total_weight() <= Decimal(30)

    def calculate_cost(self, order: models.Order) -> Decimal:
        """
            Base cost + flat rate per kg
        """
        return self.base_cost + (self.flat_rate * order.get_total_weight())

class ShippingOptionPolicy(ABC):

    @abstractmethod
    def get_shipping_options(self, order: models.Order) -> List[dict]:
        options = []
        for option in self.shipping_options:
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append({
                    "name": option.name,
                    "delivery_time": option.delivery_time,
                    "cost": float(cost)
                })
        return options

class DefaultShippingOptionPolicy(ShippingOptionPolicy):
    def __init__(self):
        self.shipping_options = [
            ShippingOption(
                name=enums.ShippingMethod.STANDARD,
                delivery_time="3-5 business days",
                base_cost=Decimal("5.00")
            ),
            ShippingOption(
                name=enums.ShippingMethod.EXPRESS,
                delivery_time="1-2 business days",
                base_cost=Decimal("15.00")
            ),
            ShippingOption(
                name=enums.ShippingMethod.SAME_DAY,
                delivery_time="same day",
                base_cost=Decimal("25.00")
            ),
            Vendor1ShippingOption(
                name=enums.ShippingMethod.FLAT_RATE,
                delivery_time="4-6 business days",
                base_cost=Decimal("10.00"),
                flat_rate=Decimal("2.00")
            )
        ]


