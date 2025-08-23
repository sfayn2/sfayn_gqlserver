from __future__ import annotations
from decimal import Decimal
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class FreeShippingOfferStrategy(ports.OfferStrategyAbstract):

    def __init__(self, strategy: value_objects.OfferStrategy):
        self.strategy = strategy

    def is_eligible(self, order: models.Order) -> bool:
        return self.strategy.conditions and self.strategy.conditions.get("minimum_order_total") and (order.total_amount.amount >= self.strategy.conditions.get("minimum_order_total"))

    def apply(self, order: models.Order):
        currency = order.currency
        zero_shipping_cost = value_objects.Money(
            amount=Decimal("0"),
            currency=currency
        )
        self.order.update_shipping_details(
                order.shipping_details.update_cost(zero_shipping_cost)
            )

        return f"{self.strategy.name} | 0 {currency}"