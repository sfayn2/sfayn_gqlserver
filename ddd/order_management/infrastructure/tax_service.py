from ddd.order_management.domain.services import tax_handler
from ddd.order_management.domain import models, value_objects
from decimal import Decimal

class TaxService(tax_handler.TaxHandlerMain):

    def __init__(self):
        self.tax_handlers = [
            tax_handler.SingaporeTaxHandler(),
            tax_handler.USStateTaxHandler()
        ]

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

        for tax_handler in self.tax_handlers:
            tax_details.append(
                tax_handler.apply_tax(order)
            )

        order.update_tax_details(tax_details)