from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.tax_strategies import ports

#Singapore Tax
class SingaporeTaxStrategy(ports.TaxStrategyAbstract):
    GST_RATE = 0.09

    def apply(self, order: models.Order):
        if order.destination.country.lower() == "singapore":
            tax_amount = order.sub_total.multiply(self.GST_RATE)
            desc = f"GST ({self.GST_RATE*100} %) | {order.tax_amount.amount} {order.tax_amount.currency}"

            return value_objects.TaxResult(amount=tax_amount, desc=desc)