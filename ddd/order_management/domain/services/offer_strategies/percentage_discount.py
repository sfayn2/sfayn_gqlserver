from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class PercentageDiscountStrategy(ports.OfferStrategyAbstract):

    #apply on order
    def apply(self, order: models.Order):
        total_discount = 0
        currency = order.currency
        discounted_items = []
        eligible_products = self.strategy.conditions.get("eligible_products")
        for item in order.line_items:
            if eligible_products and (item.product_name in eligible_products):
                total_discount += item.total_price * (self.strategy.discount_value / 100)
                discounted_items.append(item.product_name)
                total_discounts_fee = value_objects.Money(
                            amount=total_discount,
                            currency=currency
                        )

                return value_objects.OfferResult(
                    name=self.strategy.name,
                    desc=f"{self.strategy.name} | {','.join(discounted_items)} )"
                    discounts_fee=total_discounts_fee
                )
