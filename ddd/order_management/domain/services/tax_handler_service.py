from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
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

TAX_HANDLERS = [
    SingaporeTaxHandler(),
    USStateTaxHandler()
]

class TaxHandlerService:

    def apply_taxes(self, order: models.Order):
        tax_details = []
        currency = order.get_currency()

        #Reset tax amount
        order.update_tax_amount(
            value_objects.Money(
                amount=Decimal("0.0"),
                currency=currency
            )
        )

        for tax_handler in TAX_HANDLERS:
            tax_details.append(
                tax_handler.apply_tax(order)
            )

        order.update_tax_details(tax_details)

