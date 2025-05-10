from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.shipping_option_strategies import ports

class FreeShippingStrategy(ports.ShippingOptionStrategyAbstract):

    def is_eligible(self, order: models.Order) -> bool:
        #orders above $50?
        return order.sub_total > self.strategy.conditions.get("min_order_amount")

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        #default is zero
        return value_objects.Money.default()