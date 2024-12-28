from abc import ABC, abstractmethod
from typing import Optional
from ddd.order_management.domain import value_objects, models

class TaxCalculationPolicy(ABC):
    def calculate_tax(self, order: models.Order, customer: Optional[value_objects.Customer], location: Optional[value_objects.Address]):
        raise NotImplementedError("Subclasses must implement this method")

#Singapore Tax
class SGTaxCalculationPolicy(TaxCalculationPolicy):
    GST_RATE = 0.09

    def calculate_tax(self, order: models.Order):
        return order.get_total_amount * self.GST_RATE

class USTaxCalculationPolicy(TaxCalculationPolicy):
    STATE_TAX_RATES = {
        "CA": 0.075,
        "NY": 0.04,
        "TX": 0.0625
    }

    def calculate_tax(self, order: models.Order):
        state = order.destination.get_state()
        state_tax_rate = self.STATE_TAX_RATES.get(state, 0)
        return order.get_total_amount * state_tax_rate

