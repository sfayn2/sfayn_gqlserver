from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects
from decimal import Decimal

class ShippingOptionHandler(ABC):
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
    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        currency = order.get_currency()
        return value_objects.Money(
            amount=self.base_cost,
            currency=currency
        )

class ShippingOption1Handler(ShippingOptionHandler):
    def __init__(self, name: str, delivery_time: str, base_cost: Decimal, flat_rate: Decimal):
        super().__init__(name, delivery_time, base_cost)
        self.flat_rate = flat_rate

    def is_eligible(self, order: models.Order) -> bool:
        """
            Only allow packages under 30kg
        """
        return order.get_total_weight() <= Decimal(30)

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Base cost + flat rate per kg
        """
        currency = order.get_currency()
        return value_objects.Money(
            amount=self.base_cost + (self.flat_rate * order.get_total_weight()),
            currency=currency
        )

class ShippingOptionHandlerMain(ABC):

    @abstractmethod
    def get_shipping_options(self, order: models.Order) -> List[dict]:
        raise NotImplementedError("Subclasses must implement this method")