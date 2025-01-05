from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class TaxStrategy(ABC):
    def apply(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

#Singapore Tax
class SingaporeTaxStrategy(TaxStrategy):
    GST_RATE = 0.09

    def apply(self, order: models.Order):
        if order.destination.country.lower() == "singapore":
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

TAX_STRATEGIES = [
    SingaporeTaxStrategy(),
    USStateTaxStrategy()
]

class TaxStrategyService:

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

        for tax_strategy in TAX_STRATEGIES:
            tax_details.append(
                tax_strategy.apply(order)
            )

        order.update_tax_details(tax_details)

