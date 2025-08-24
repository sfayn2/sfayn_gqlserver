from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.shipping_option_strategies import ports


class ExpressShippingStrategy(ports.ShippingOptionStrategyAbstract):

    def __init__(self, strategy: value_objects.ShippingOptionStrategy, clock: ClockAbstract):
        self.strategy = strategy
        self.clock = clock

    def is_before_cutoff(self):
        return self.clock.now() <= self.strategy.conditions.get("cutoff_time")

    def is_eligible(self, order: models.Order) -> bool:
        return order.total_weight <= self.strategy.conditions.get("max_weight") and self.is_before_cutoff()

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        return self.strategy.base_cost.add(self.strategy.flat_rate.multiply(order.total_weight))