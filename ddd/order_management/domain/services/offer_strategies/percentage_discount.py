from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class PercentageDiscountStrategy(ports.OfferStrategyAbstract):

    #apply on order
    def apply(self):
        total_discount = 0
        currency = self.order.currency
        discounted_items = []
        eligible_products = self.strategy.conditions.get("eligible_products")
        required_coupon = self.strategy.conditions.get("required_coupon")
        if required_coupon == False:
            for item in self.order.line_items:
                if eligible_products and item.product_sku in eligible_products:
                    if total_discount == 0:
                        total_discount = item.total_price.multiply(self.strategy.discount_value / 100)
                    else:
                        total_discount = total_discount.add(
                            item.total_price.multiply(self.strategy.discount_value / 100)
                        )
                    discounted_items.append(item.product_sku)

            if discounted_items:
                self.order.update_total_discounts_fee(total_discount.format())
                return f"{self.strategy.name} | {','.join(discounted_items)} | {total_discount.format().amount}"
