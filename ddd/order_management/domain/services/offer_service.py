from __future__ import annotations
import pytz
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class OfferStrategy(ABC):
    def __init__(self, strategy: value_objects.OfferStrategy):
        self.strategy = strategy

    @abstractmethod
    def apply(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_coupon(self, order: models.Order):
        #reuse if the offer is based on coupon
        for coupon in order.coupons:
            if self.strategy.required_coupon == True and coupon in [item for item in self.coupons]:
                return True
        return False

    def validate_minimum_quantity(self, order:models.Order):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_quantity") and (sum(item.order_quantity for item in order.line_items) >= self.stategy.conditions.get("minimum_quantity"))

    def validate_minimum_order_total(self, order:models.Order):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_order_total") and (order.total_amount.amount >= self.stategy.conditions.get("minimum_order_total"))

class PercentageDiscountStrategy(OfferStrategy):

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
                #item.set_discounts_fee(value_objects.Money(
                #    amount=total_discount,
                #    currency=currency
                #))
                order.update_total_discounts_fee(
                        value_objects.Money(
                            amount=total_discount,
                            currency=currency
                        )
                    )
                return f"{self.name} | {','.join(discounted_items)} )"

class FreeGiftOfferStrategy(OfferStrategy):

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
                return f"{self.description} | {','.join(free_gifts)}"
    
class FreeShippingOfferStrategy(OfferStrategy):

    def apply(self, order: models.Order):
        currency = order.currency
        if self.validate_minimum_order_total(order) and self.validate_coupon(order):
            zero_shipping_cost = value_objects.Money(
                amount=Decimal("0"),
                currency=currency
            )
            order.update_shipping_details(
                    order.shipping_details.update_cost(zero_shipping_cost)
                )

            return f"{self.name} | 0 {currency}"



class PercentageDiscountCouponOfferStrategy(OfferStrategy):

    def apply(self, order: models.Order):
        total_discount = 0
        discounted_items = []
        currency = order.currency
        eligible_products = self.strategy.conditions.get("eligible_products")

        if self.validate_coupon(order):
            for item in order.line_items:
                if eligible_products and item.product_name in eligible_products:
                    total_discount += item.total_price * (self.strategy.discount_value / 100)
                    discounted_items.append(item.product_name)

                    order.update_total_discounts_fee(
                            value_objects.Money(
                                amount=total_discount,
                                currency=currency
                            )
                        )
                    return f"{self.name} | {','.join(discounted_items)}"


# when adding new offer need to map the strategy
OFFER_STRATEGIES = {
    enums.OfferType.PERCENTAGE_DISCOUNT: PercentageDiscountStrategy,
    enums.OfferType.FREE_GIFT: FreeGiftOfferStrategy,
    enums.OfferType.COUPON_PERCENTAGE_DISCOUNT: PercentageDiscountCouponOfferStrategy,
    enums.OfferType.FREE_SHIPPING: FreeShippingOfferStrategy
}

class OfferStrategyService:        

    def __init__(self, vendor_repository: repositories.VendorRepository):
        self.vendor_repository = vendor_repository

    def apply_offers(self, order: models.Order):
        if not order.shipping_details:
            raise exceptions.InvalidOrderOperation("Only when shipping option is selected.")
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
        sorted_vendor_offers = sorted(vendor_offers, key=lambda x: x["priority"], reverse=True)

        for offer in sorted_vendor_offers:

            offer_strategy_class = OFFER_STRATEGIES.get(offer.get("offer_type"))

            offer_strategy = value_objects.OfferStrategy(**{
                **offer,
                "coupons":[value_objects.Coupon(**coupon) for coupon in offer.get("coupons")]
            })

            if offer_strategy.is_valid:
                valid_offers.append(
                    offer_strategy_class(offer_strategy)
                )

                if offer.get("stackable") == False:
                    #make sure offers already ordered based on highest priority, so checking stackable is enough
                    return valid_offers

        return valid_offers
