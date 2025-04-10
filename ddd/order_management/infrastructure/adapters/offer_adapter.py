from __future__ import annotations
import pytz
from datetime import datetime
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal
from ddd.order_management.application import ports


# =========================
# Offer Strategies
# ====================
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
                order.update_total_discounts_fee(
                        value_objects.Money(
                            amount=total_discount,
                            currency=currency
                        )
                    )
                return f"{self.strategy.name} | {','.join(discounted_items)} )"

class FreeGiftOfferStrategy(ports.OfferStrategyAbstract):

    def apply(self, order: models.Order):
        free_gifts = []
        currency = order.currency
        gift_products = self.strategy.conditions.get("gift_products")
        if self.validate_minimum_quantity(order):
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
                return f"{self.strategy.name} | {','.join(free_gifts)}"
    
class FreeShippingOfferStrategy(ports.OfferStrategyAbstract):

    def apply(self, order: models.Order):
        currency = order.currency
        #if self.validate_minimum_order_total(order) and self.validate_coupon(order):
        if self.validate_minimum_order_total(order):
            zero_shipping_cost = value_objects.Money(
                amount=Decimal("0"),
                currency=currency
            )
            order.update_shipping_details(
                    order.shipping_details.update_cost(zero_shipping_cost)
                )

            return f"{self.strategy.name} | 0 {currency}"



class PercentageDiscountCouponOfferStrategy(ports.OfferStrategyAbstract):

    def apply(self, order: models.Order):
        total_discount = 0
        discounted_items = []
        eligible_products = self.strategy.conditions.get("eligible_products")

        if self.validate_coupon(order):
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

                    return f"{self.strategy.name} | {','.join(discounted_items)} | {total_discount.amount} {total_discount.currency}"

# ==============
# Offer Strategy Mapper
# ===============

# when adding new offer need to map the strategy
OFFER_STRATEGIES = {
    enums.OfferType.PERCENTAGE_DISCOUNT: PercentageDiscountStrategy,
    enums.OfferType.FREE_GIFT: FreeGiftOfferStrategy,
    enums.OfferType.COUPON_PERCENTAGE_DISCOUNT: PercentageDiscountCouponOfferStrategy,
    enums.OfferType.FREE_SHIPPING: FreeShippingOfferStrategy
}

# ================
# Offer Strategy Service
# ==================

class OfferStrategyService(ports.OfferStrategyServiceAbstract):        

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    def apply_offers(self, order: models.Order):
        available_offers = self._fetch_valid_offers(order.vendor_name)
        offer_details = []
        for strategy in available_offers:
            res = strategy.apply(order)
            if res:
                offer_details.append(res)

        if offer_details:
            order.update_offer_details(offer_details)

    def _fetch_valid_offers(self, vendor_name: str):
        #The assumption is all Offers are auto applied (except those w Coupons)
        vendor_offers = self.vendor_repository.get_offers(vendor_name)
        valid_offers = []

        #sorted by "priority" in descending order
        sorted_vendor_offers = sorted(vendor_offers, key=lambda vo: vo.priority, reverse=True)

        for offer in sorted_vendor_offers:

            offer_strategy_class = OFFER_STRATEGIES.get(offer.offer_type)
            valid_offers.append(
                offer_strategy_class(offer)
            )

            if offer.stackable == False:
                #make sure offers already ordered based on highest priority, so checking stackable is enough
                return valid_offers

        return valid_offers
