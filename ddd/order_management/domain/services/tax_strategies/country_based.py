from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.tax_strategies import ports

class CountryBasedTaxStrategy(ports.TaxStrategyAbstract):

    def __init__(self, strategy: value_objects.TaxStrategy):
        self.strategy = strategy

    def is_eligible(self, order: models.Order) -> bool:
        return order.destination.country.lower() == self.strategy.conditions.get("country")

    def calculate_tax(self, order: models.Order) -> value_objects.TaxResult:
        tax_amount = order.sub_total.multiply(self.strategy.RATE).format()
        desc = f"{self.strategy.tax_type} ({self.strategy.RATE*100} %) | {tax_amount.amount} {tax_amount.currency}"

        return value_objects.TaxResult(amount=tax_amount, desc=desc)