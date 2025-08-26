from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.shipping_option_strategies import ports
from ddd.order_management.domain.services import DomainClock

class LocalPickupShippingStrategy(ports.ShippingOptionStrategyAbstract):

    def __init__(self, strategy: value_objects.ShippingOptionStrategy):
        self.strategy = strategy

    def is_near_by(self, order: models.Order):
        return (order.destination.city in self.strategy.conditions.get("near_by_cities") and 
                order.destination.country == order.vendor_country
        )

    def is_eligible(self, order: models.Order) -> bool:
        current_time = DomainClock.now()
        return (current_time >= self.strategy.conditions.get("pickup_time_from") and 
                current_time <= self.strategy.conditions.get("pickup_time_to") and
                self.is_near_by(order)
        )

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        #default is zero
        return value_objects.Money.default()