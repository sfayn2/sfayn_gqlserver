from __future__ import annotations
import json
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union
from ddd.order_management.domain import enums, exceptions, models, value_objects, repositories
from decimal import Decimal

class OfferHandler(ABC):
    def __init__(self, offer_type: enums.OfferType, description: str, 
                 conditions: dict, start_date: datetime, end_date: datetime, 
                 discount_value: Union[int, Decimal], required_coupon: bool, 
                 coupon_code: str, stackable: bool, priority: int):
        self.offer_type = offer_type
        self.description = description
        self.conditions = conditions
        self.start_date = start_date
        self.end_date = end_date
        self.discount_value = discount_value

    @abstractmethod
    def apply_offer(self, order: models.Order) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class PercentageDiscountHandler(OfferHandler):

    #apply on order
    def apply_offer(self, order: models.Order) -> str:
        total_discount = 0
        is_applied = False
        currency = order.get_currency()
        discounted_items = []
        eligible_products = self.conditions.get("eligible_products")
        for item in order.line_items:
            if eligible_products and (item.get_product_name() in eligible_products):
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

class FreeGiftOfferHandler(OfferHandler):

    def apply_offer(self, order: models.Order) -> str:
        free_gifts = []
        currency = order.get_currency()
        is_applied = False
        minimum_quantity = self.conditions.get("minimum_quantity")
        gift_products = self.conditions.get("gift_products")
        if minimum_quantity and (sum(item.order_quantity for item in order.line_items) >= minimum_quantity):
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
                is_applied = True

        if is_applied:
            return f"{self.description} applied ( {','.join(free_gifts)} )"
    
class FreeShippingOfferHandler(OfferHandler):

    def apply_offer(self, order: models.Order) -> str:
        is_applied = False
        currency = order.get_currency()
        minimum_order_total = self.conditions.get("minimum_order_total")
        if minimum_order_total and (order.get_total_amount().amount >= minimum_order_total):
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

class PercentageDiscountCouponOfferHandler(OfferHandler):

    def apply_offer(self, order: models.Order) -> value_objects.Money:
        total_discount = 0
        discounted_items = []
        currency = order.get_currency()
        is_applied = False
        eligible_products = self.conditions.get("eligible_products")
        start_date = self.conditions.get("start_date")
        end_date = self.conditions.get("end_date")
        requires_coupon = self.conditions.get("requires_coupon")
        coupon_code = self.conditions.get("coupon_code")

        if requires_coupon == True and (datetime.now() >= start_date and datetime.now() <= end_date):
            if coupon_code in order.get_customer_coupons():
                for item in order.line_items:
                    if eligible_products and item.get_product_name() in eligible_products:
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

# when adding new offer need to map the handler
OFFERS_HANDLER = {
    enums.OfferType.PERCENTAGE_DISCOUNT.name: PercentageDiscountHandler,
    enums.OfferType.FREE_GIFT.name: FreeGiftOfferHandler,
    enums.OfferType.COUPON_DISCOUNT: PercentageDiscountCouponOfferHandler,
    enums.OfferType.FREE_SHIPPING: FreeShippingOfferHandler
}

class OfferHandlerService(ABC):        

    def __init__(self, vendor_repository: repositories.VendorRepository):
        self.vendor_repository = vendor_repository

    def apply_offers(self, order: models.Order):
        available_offers = self._fetch_valid_offers(order.vendor)
        offer_details = []
        for offer_handler in available_offers:
            offer_details.append(
                offer_handler.apply_offer(order)
            )

        order.update_offer_details(offer_details)

    def _fetch_valid_offers(self, vendor_name: str):
        vendor_offers = self.vendor_repository.get_offers(vendor_name)
        valid_offers = []
        for offer in vendor_offers:

            #handler function
            offer_handler_class = OFFERS_HANDLER.get(offer.get("offer_type"))

            if offer_handler_class:
                valid_offers.append(
                    offer_handler_class(
                        offer_type=enums.OfferType[offer.get("offer_type")],
                        description=offer.get("name"),
                        discount_value=offer.get("discount_value"),
                        condition=json.loads(offer.get("conditions")),
                        required_coupon=offer.get("required_coupon"),
                        coupon_code=json.loads(offer.get("coupon_code")),
                        stackable=offer.get("stackable"),
                        priority=offer.get("priority"),
                        start_date=offer.get("start_date"),
                        end_date=offer.get("end_date")
                    )
                )

        return valid_offers



