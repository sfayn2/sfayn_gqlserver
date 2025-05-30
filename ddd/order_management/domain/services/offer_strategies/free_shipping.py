from __future__ import annotations
from decimal import Decimal
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class FreeShippingOfferStrategy(ports.OfferStrategyAbstract):

    def apply(self, order: models.Order):
        currency = order.currency
        #if self.validate_minimum_order_total(order) and self.validate_coupon(order):
        if self.validate_minimum_order_total(order):
            #zero_shipping_cost = value_objects.Money(
            #    amount=Decimal("0"),
            #    currency=currency
            #)
            #order.update_shipping_details(
            #        order.shipping_details.update_cost(zero_shipping_cost)
            #    )

            return value_objects.OfferResult(
                name=self.strategy.name,
                desc=f"{self.strategy.name} | 0 {currency}",
                free_shipping=True
            )