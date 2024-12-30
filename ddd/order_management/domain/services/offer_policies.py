from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union
from ddd.order_management.domain import enums, exceptions, models, value_objects
from decimal import Decimal

class BaseOffer(ABC):
    def __init__(self, offer_type: enums.OfferType, description: str):
        self.offer_type = offer_type
        self.description = description

    @abstractmethod
    def apply_offer(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

class OfferPolicy(ABC):

    @abstractmethod
    def apply_all_offers(self, order: models.Order):
        applied_offers = []
        for offer in self.offers:
            applied_offers.append(
                offer().apply_offer(order)
            )

        return "\n".join(applied_offers)

class DiscountOffer(BaseOffer):
    def __init__(self, offer_type: enums.OfferType, description: str, discount_type: enums.DiscountType, discount_value: Decimal, eligible_products: List[str]):
        super().__init__(offer_type, description)
        self.discount_type = discount_type 
        self.discount_value = discount_value
        self.eligible_products = eligible_products

    #apply on order
    def apply_offer(self, order: models.Order) -> value_objects.Money:
        total_discount = 0
        is_applied = False
        currency = order.get_currency()
        discounted_items = []
        for item in order.line_items:
            if item.get_product_name() in self.eligible_products:
                total_discount += item.get_total_price() * (self.discount_value / 100)
                is_applied = True
                discounted_items.append(item.get_product_name())
                #item.set_discounts_fee(value_objects.Money(
                #    amount=total_discount,
                #    currency=currency
                #))
        if is_applied:
            order.update_total_discounts_fee(
                    value_objects.Money(
                        amount=total_discount,
                        currency=currency
                    )
                )
            return f"{self.description} applied ( {','.join(discounted_items)} )"

class FreeGiftOffer(BaseOffer):
    def __init__(self, offer_type: enums.OfferType, description: str, min_quantity: int, gift_products: List[dict]):
        super().__init__(offer_type, description)
        self.min_quantity = min_quantity 
        self.gift_products = gift_products

    def apply_offer(self, order: models.Order):
        free_gifts = []
        currency = order.get_currency()
        is_applied = False
        if sum(item.order_quantity for item in order.line_items) >= self.min_quantity:
            for free_product in self.gift_products:
                free_gifts.append(free_product)

                # add free product gifts
                order.add_line_item(
                    value_objects.LineItem(
                        _product_sku=free_product.get('sku'),
                        _product_price=value_objects.Money(0, currency),
                        _order_quantity=free_product.get('quantity'),
                        _is_free_gift=True
                    )
                )
                is_applied = True

        if is_applied:
            return f"{self.description} applied ( {','.join(free_gifts)} )"
    
class FreeShippingOffer(BaseOffer):
    def __init__(self, offer_type: enums.OfferType, description: str, min_order_total: int):
        super().__init__(offer_type, description)
        self.min_order_total = min_order_total 

    def apply_offer(self, order: models.Order):
        is_applied = False
        currency = order.get_currency()
        if order.get_total_amount().amount >= self.min_order_total:
            _shipping_cost = value_objects.Money(
                amount=0,
                currency=currency
            )

            #shipping cost waived?
            order.update_shipping_details(value_objects.ShippingDetails(
                    method=order.shipping_details.method,
                    delivery_time=order.shipping_details.delivery_time,
                    cost=_shipping_cost
                )
            )

            is_applied = True

        if is_applied:
            return f"{self.description} applied"

class DiscountCouponOffer(BaseOffer):
    def __init__(self, offer_type: enums.OfferType, description: str, coupon_code: str, min_order_total: Decimal, requires_coupon: bool, expiry_date: DateTime):
        super().__init__(offer_type, description)
        self.coupon_code = coupon_code
        self.min_order_total = min_order_total
        self.expiry_date = expiry_date
        self.requires_coupon = requires_coupon

    def apply_offer(self, order: models.Order) -> value_objects.Money:
        total_discount = 0
        discounted_items = []
        currency = order.get_currency()
        is_applied = False
        #TODO to simplify, hard coded the expiration date. future plan to move expirate_date, usage_limit to db?
        if self.requires_coupon and self.expiry_date >= datetime.date():
            if self.coupon_code in order.get_customer_coupons():
                return

            for item in order.line_items:
                if item.get_product_name() in self.eligible_products:
                    total_discount += item.get_total_price() * (self.discount_value / 100)
                    discounted_items.append(item.get_product_name())
                    is_applied = True

            if is_applied:
                order.update_total_discounts_fee(
                        value_objects.Money(
                            amount=total_discount,
                            currency=currency
                        )
                    )
                return f"{self.description} applied ( {','.join(discounted_items)} )"



class DefaultOfferPolicy(OfferPolicy):
    def __init__(self):
        self.offers = [
            DiscountOffer(
                offer_type=enums.OfferType.DISCOUNT,
                description="10% off Lacoste Product",
                discount_type=enums.DiscountType.PERCENTAGE,
                discount_value=Decimal("10"),
                eligible_products=["Lacoste"]
            ),
            DiscountCouponOffer(
                offer_type=enums.OfferType.DISCOUNT,
                description="10% off w WELCOME25",
                discount_type=enums.DiscountType.PERCENTAGE,
                discount_value=Decimal("10"),
                eligible_products=["Lacoste"],
                coupon_code="WELCOME25",
                expiry_date="12/31/2024",
                requires_coupon=True
            ),
            FreeGiftOffer(
                offer_type=enums.OfferType.FREE_GIFT,
                description="Free gift for 2+ items",
                min_quantity=2,
                gift_products=[{"sku": "123", "quantity": 1}]
            ),
            FreeShippingOffer(
                offer_type=enums.OfferType.FREE_SHIPPING,
                description="Free shipping for orders above $150",
                min_order_total=150
            )
        ]





