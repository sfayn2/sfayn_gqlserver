from __future__ import annotations
import json
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class OfferStrategy(ABC):
    def __init__(self, offer_type: enums.OfferType, description: str, 
                 conditions: dict, start_date: datetime, end_date: datetime, 
                 discount_value: Union[int, Decimal], required_coupon: bool, 
                 coupon_code: str):
        self.offer_type = offer_type
        self.description = description
        self.conditions = conditions
        self.start_date = start_date
        self.end_date = end_date
        self.discount_value = discount_value
        self.required_coupon = required_coupon
        self.coupon_code = coupon_code

    @abstractmethod
    def apply(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_coupon(self, order: models.Order):
        #reuse if the offer is based on coupon
        return (self.requires_coupon == True
            and (datetime.now() >= self.start_date and datetime.now() <= self.end_date)
            and self.coupon_code in order.customer_coupons
        )

    def validate_minimum_quantity(self, order:models.Order):
        return self.minimum_quantity and (sum(item.order_quantity for item in order.line_items) >= self.minimum_quantity)

    def validate_minimum_order_total(self, order:models.Order):
        return self.minimum_order_total and (order.total_amount.amount >= self.minimum_order_total)

class PercentageDiscountStrategy(OfferStrategy):

    #apply on order
    def apply(self, order: models.Order):
        total_discount = 0
        currency = order.currency
        discounted_items = []
        eligible_products = self.conditions.get("eligible_products")
        for item in order.line_items:
            if eligible_products and (item.product_name in eligible_products):
                total_discount += item.total_price * (self.discount_value / 100)
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
                return f"{self.description} applied ( {','.join(discounted_items)} )"

class FreeGiftOfferStrategy(OfferStrategy):

    def apply(self, order: models.Order):
        free_gifts = []
        currency = order.currency
        gift_products = self.conditions.get("gift_products")
        if self.validate_minimum_quantity(order):
            for free_product in gift_products:
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
                return f"{self.description} applied ( {','.join(free_gifts)} )"
    
class FreeShippingOfferStrategy(OfferStrategy):

    def apply(self, order: models.Order):
        currency = order.currency
        if self.validate_minimum_order_total(order):
            zero_shipping_cost = value_objects.Money(
                amount=0,
                currency=currency
            )
            order.update_shipping_details(
                    order.shipping_details.update_cost(zero_shipping_cost)
                )

            return f"{self.description} applied"



class PercentageDiscountCouponOfferStrategy(OfferStrategy):

    def apply(self, order: models.Order):
        total_discount = 0
        discounted_items = []
        currency = order.currency
        eligible_products = self.conditions.get("eligible_products")

        if self.validate_coupon(order):
            for item in order.line_items:
                if eligible_products and item.product_name in eligible_products:
                    total_discount += item.total_price * (self.discount_value / 100)
                    discounted_items.append(item.product_name)

                    order.update_total_discounts_fee(
                            value_objects.Money(
                                amount=total_discount,
                                currency=currency
                            )
                        )
                    return f"{self.description} applied ( {','.join(discounted_items)} )"


# when adding new offer need to map the strategy
OFFER_STRATEGIES = {
    enums.OfferType.PERCENTAGE_DISCOUNT.name: PercentageDiscountStrategy,
    enums.OfferType.FREE_GIFT.name: FreeGiftOfferStrategy,
    enums.OfferType.COUPON_DISCOUNT.name: PercentageDiscountCouponOfferStrategy,
    enums.OfferType.FREE_SHIPPING.name: FreeShippingOfferStrategy
}

class OfferStrategyService:        

    def __init__(self, vendor_repository: repositories.VendorRepository):
        self.vendor_repository = vendor_repository

    def apply_offers(self, order: models.Order):
        if not self.order.shipping_details:
            raise exceptions.InvalidOrderOperation("Only when shipping option is selected.")
        available_offers = self._fetch_valid_offers(order.vendor)
        offer_details = []
        for strategy in available_offers:
            offer_details.append(
                strategy.apply(order)
            )

        order.update_offer_details(offer_details)

    def _fetch_valid_offers(self, vendor_name: str):
        #The assumption is all Offers are auto applied (except those w Coupons)
        vendor_offers = self.vendor_repository.get_offers(vendor_name)
        valid_offers = []

        #sorted by "priority" in descending order
        sorted_vendor_offers = sorted(vendor_offers, key=lambda x: x["priority"], reverse=True)

        for offer in sorted_vendor_offers:

            #strategy function
            offer_strategy_class = OFFER_STRATEGIES.get(offer.get("offer_type"))

            if offer_strategy_class:

                valid_offers.append(
                    offer_strategy_class(
                            offer_type=enums.OfferType[offer.get("offer_type")],
                            description=offer.get("name"),
                            discount_value=offer.get("discount_value"),
                            condition=json.loads(offer.get("conditions")),
                            required_coupon=offer.get("required_coupon"),
                            coupon_code=json.loads(offer.get("coupon_code")),
                            start_date=offer.get("start_date"),
                            end_date=offer.get("end_date")
                        )
                )

                if offer.get("stackable") == False:
                    #make sure offers already ordered based on highest priority, so checking stackable is enough
                    return valid_offers

        return valid_offers



