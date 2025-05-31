from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class PercentageDiscountCouponOfferStrategy(ports.OfferStrategyAbstract):

    def apply(self):
        total_discount = 0
        discounted_items = []
        eligible_products = self.strategy.conditions.get("eligible_products")

        if self.validate_coupon():
            for item in self.order.line_items:
                if eligible_products and item.product_sku in eligible_products:
                    if total_discount == 0:
                        total_discount = item.total_price.multiply(self.strategy.discount_value / 100)
                    else:
                        total_discount = total_discount.add(
                            item.total_price.multiply(self.strategy.discount_value / 100)
                        )
                    discounted_items.append(item.product_sku)

                    self.order.update_total_discounts_fee(total_discount)

            return f"{self.strategy.name} | {','.join(discounted_items)} | {total_discount.amount} {total_discount.currency}"

                    #return value_objects.OfferResult(
                    #    name=self.strategy.name,
                    #    desc=f"{self.strategy.name} | {','.join(discounted_items)} | {total_discount.amount} {total_discount.currency}",
                    #    discounts_fee=total_discount
                    #)
