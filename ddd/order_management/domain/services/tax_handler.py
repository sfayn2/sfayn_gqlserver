from abc import ABC, abstractmethod
from typing import Optional
from ddd.order_management.domain import value_objects, models

class TaxHandler(ABC):
    def apply_tax(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

#Singapore Tax
class SingaporeTaxHandler(TaxHandler):
    GST_RATE = 0.09

    def apply_tax(self, order: models.Order):
        if order.destination.get_country().lower() == "singapore":
            current_tax = order.get_tax_amount()
            tax_amount = order.get_total_amount().add(
                    order.shipping_details.cost
                ).multiply(self.GST_RATE)

            if current_tax:
                order.update_tax_amount(
                        tax_amount.add(current_tax)
                    )
            else:
                order.update_tax_amount(tax_amount)

            return f"GST ({self.GST_RATE*100} %) : {order.get_tax_amount()}"

class USStateTaxHandler(TaxHandler):
    STATE_TAX_RATES = {
        "CA": 0.075,
        "NY": 0.04,
        "TX": 0.0625
    }

    def apply_tax(self, order: models.Order):
        if order.destination.get_country().lower() == "united states":
            state = order.destination.get_state()
            state_tax_rate = self.STATE_TAX_RATES.get(state, 0)
            current_tax = order.get_tax_amount()
            tax_amount = order.get_total_amount().add(
                    order.shipping_details.cost
                ).multiply(state_tax_rate)

            if current_tax:
                order.update_tax_amount(
                        tax_amount.add(current_tax)
                    )
            else:
                order.update_tax_amount(tax_amount)

            return f"{state} State Tax ({state_tax_rate*100} %) : {order.get_tax_amount()}"

class TaxHandlerMain(ABC):

    @abstractmethod
    def apply_taxes(self):
        raise NotImplementedError("Subclasses must implement this method")

