from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.tax_strategies import ports

class StateBasedTaxStrategy(ports.TaxStrategyAbstract):
    #STATE_TAX_RATES = {
    #    "CA": 0.075,
    #    "NY": 0.04,
    #    "TX": 0.0625
    #}

    def __init__(self, strategy: value_objects.TaxStrategy):
        self.strategy = strategy

    def is_eligible(self, order: models.Order) -> bool:
        return order.destination.country.lower() == self.strategy.conditions.get("country") and self.strategy.conditions.get("state_tax_rates")

    def calculate_tax(self, order: models.Order):
        state = order.destination.state
        state_tax_rate = self.strategy.condition.get("state_tax_rates").get(state)
        tax_amount = order.sub_total.multiply(state_tax_rate).format()
        desc = f"{self.strategy.tax_type} ({state_tax_rate*100} %) | {tax_amount.amount} {tax_amount.currency}"

        return value_objects.TaxResult(amount=tax_amount, desc=desc)
