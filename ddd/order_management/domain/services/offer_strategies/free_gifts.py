from __future__ import annotations
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services.offer_strategies import ports

class FreeGiftsOfferStrategy(ports.OfferStrategyAbstract):

    def __init__(self, strategy: value_objects.OfferStrategy):
        self.strategy = strategy

    def is_eligible(self, order: models.Order) -> bool:
        return self.strategy.conditions and self.strategy.conditions.get("minimum_quantity") and (sum(item.order_quantity for item in order.line_items) >= self.strategy.conditions.get("minimum_quantity"))

    def apply(self, order: models.Order):
        free_gifts = []
        currency = order.currency
        gift_products = self.strategy.conditions.get("gift_products")

        for free_product in gift_products:
            free_gifts.append(free_product)

            # add free product gifts
            order.add_line_item(
                value_objects.LineItem(
                    product_sku=free_product.get('sku'),
                    product_price=value_objects.Money(0, currency),
                    order_quantity=free_product.get('quantity'),
                    is_free_gift=True
                )
            )

        if free_gifts:
            return f"{self.strategy.name} | {','.join(free_gifts)}"
