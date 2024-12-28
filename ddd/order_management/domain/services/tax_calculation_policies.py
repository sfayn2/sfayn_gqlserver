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
        return {
            "desc": f"GST ({self.GST_RATE * 100} %)", 
            "total_tax":order.get_total_amount * self.GST_RATE 
        }

class USTaxCalculationPolicy(TaxCalculationPolicy):
    STATE_TAX_RATES = {
        "CA": 0.075,
        "NY": 0.04,
        "TX": 0.0625
    }

    def calculate_tax(self, order: models.Order):
        state = order.destination.get_state()
        state_tax_rate = self.STATE_TAX_RATES.get(state, 0)
        return {
            "desc": f"{state} State Tax ({state_tax_rate * 100} %)", 
            "total_tax":order.get_total_amount * state_tax_rate 
        }

class TaxCalculationPolicyFactory:
    def get_tax_policy(order: models.Order):
        country = order.destination.get_country().lower()
        if country == "singapore":
            return SGTaxCalculationPolicy()
        elif country == "united states":
            return USTaxCalculationPolicy()
        else:
            return ValueError(f"Tax calculation for {country} not supported.")
