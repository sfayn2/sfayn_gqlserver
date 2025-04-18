import pytz
from datetime import datetime
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.tax_strategies import ports

def _get_current_time():
    return datetime.now(pytz.utc).time()

class ExpressShippingStrategy(ports.ShippingOptionStrategyAbstract):

    def is_before_cutoff(self):
        return _get_current_time() <= self.strategy.conditions.get("cutoff_time")

    def is_eligible(self, order: models.Order) -> bool:
        return order.total_weight <= self.strategy.conditions.get("max_weight") and self.is_before_cutoff()

    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        return self.strategy.base_cost.add(self.strategy.flat_rate.multiply(order.total_weight))