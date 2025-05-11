from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.tax_strategies import ports

class USStateTaxStrategy(ports.TaxStrategyAbstract):
    STATE_TAX_RATES = {
        "CA": 0.075,
        "NY": 0.04,
        "TX": 0.0625
    }

    def calculate_tax(self, order: models.Order):
        if order.destination.country.lower() == "united states":
            state = order.destination.state
            state_tax_rate = self.STATE_TAX_RATES.get(state, 0)
            tax_amount = order.sub_total.multiply(state_tax_rate).format()
            desc = f"{state} State Tax ({state_tax_rate*100} %) | {tax_amount.amount} {tax_amount.currency}"

            return value_objects.TaxResult(amount=tax_amount, desc=desc)
