from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class TaxStrategy(ABC):
    def apply(self, order: models.Order) -> value_objects.TaxResult:
        raise NotImplementedError("Subclasses must implement this method")

#Singapore Tax
class SingaporeTaxStrategy(TaxStrategy):
    GST_RATE = 0.09

    def apply(self, order: models.Order):
        if order.destination.country.lower() == "singapore":
            tax_amount = order.sub_total.multiply(self.GST_RATE)
            desc = f"GST ({self.GST_RATE*100} %) | {order.tax_amount.amount} {order.tax_amount.currency}"

            return value_objects.TaxResult(amount=tax_amount, desc=desc)


class USStateTaxStrategy(TaxStrategy):
    STATE_TAX_RATES = {
        "CA": 0.075,
        "NY": 0.04,
        "TX": 0.0625
    }

    def apply(self, order: models.Order):
        if order.destination.country.lower() == "united states":
            state = order.destination.state
            state_tax_rate = self.STATE_TAX_RATES.get(state, 0)
            tax_amount = order.sub_total.multiply(state_tax_rate)
            desc = f"{state} State Tax ({state_tax_rate*100} %) | {order.tax_amount.amount} {order.tax_amount.currency}"

            return value_objects.TaxResult(amount=tax_amount, desc=desc)

TAX_STRATEGIES = [
    SingaporeTaxStrategy(),
    USStateTaxStrategy()
]
