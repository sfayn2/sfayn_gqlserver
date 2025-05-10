from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.shipping_option_strategies import ports

class StandardShippingStrategy(ports.ShippingOptionStrategyAbstract):

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
