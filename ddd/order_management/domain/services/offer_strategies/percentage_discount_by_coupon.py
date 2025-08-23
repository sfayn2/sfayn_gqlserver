from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class PercentageDiscountCouponOfferStrategy(ports.OfferStrategyAbstract):

    def __init__(self, strategy: value_objects.OfferStrategy):
        self.strategy = strategy

    def is_eligible(self, order: models.Order) -> bool:
        for coupon in order.coupons:
            if self.strategy.required_coupon == True and coupon in [item for item in self.strategy.coupons]:
                return True
        return False

    def apply(self, order: models.Order):
        total_discount = 0
        discounted_items = []
        eligible_products = self.strategy.conditions.get("eligible_products")

        for item in order.line_items:
            if eligible_products and item.product_sku in eligible_products:
                if total_discount == 0:
                    total_discount = item.total_price.multiply(self.strategy.discount_value / 100)
                else:
                    total_discount = total_discount.add(
                        item.total_price.multiply(self.strategy.discount_value / 100)
                    )
                discounted_items.append(item.product_sku)

                order.update_total_discounts_fee(total_discount)

        if discounted_items:
            order.update_total_discounts_fee(total_discount.format())
            return f"{self.strategy.name} | {','.join(discounted_items)} | {total_discount.format().amount}"
