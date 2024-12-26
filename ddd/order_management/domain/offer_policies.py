from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple, List
from ddd.order_management.domain import enums, exceptions, models, value_objects
from decimal import Decimal

class OfferOption(ABC):
    def __init__(self, offer_type: enums.OfferType, description: str):
        self.offer_type = offer_type
        self.description = description

    @abstractmethod
    def apply_offer(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

class OfferPolicy(ABC):
    @abstractmethod
    def get_offers(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

class DiscountOfferOption(OfferOption):
    def __init__(self, offer_type: enums.OfferType, description: str, discount_type: enums.DiscountType, discount_value: Decimal, eligible_products: List[str]):
        super().__init__(offer_type, description)
        self.discount_type = discount_type 
        self.discount_value = discount_value
        self.eligible_products = eligible_products

    #apply on order
    def apply_offer(self, order: models.Order):
        total_discount = 0
        for item in order.get_line_items():
            if item.get_product_name() in self.eligible_products:
                total_discount += item.get_total_price() * (self.discount_value / 100)
        return total_discount

class FreeGiftOfferOption(OfferOption):
    def __init__(self, offer_type: enums.OfferType, description: str, min_quantity: int, gift_product_ids: List[str]):
        super().__init__(offer_type, description)
        self.min_quantity = min_quantity 
        self.gift_products_ids = gift_product_ids

    def apply_offer(self, order: models.Order):
        free_gifts = []
        if sum(item.get_order_quantity() for item in order.get_line_items()) >= self.min_quantity:
            for prod in self.gift_products_ids:
                free_gifts.append({"product_id": prod, "quantity": 1})
        return free_gifts
    
class FreeShippingOfferOption(OfferOption):
    def __init__(self, offer_type: enums.OfferType, description: str, min_order_total: int):
        super().__init__(offer_type, description)
        self.min_order_total = min_order_total 

    def apply_offer(self, order: models.Order):
        if order.get_total_amount >= self.min_order_total:
            return 0 #shipping cost waived?
        return None


class StandardOfferPolicy(OfferPolicy):
    def __init__(self):
        self.offers = [
            DiscountOfferOption(
                offer_type=enums.OfferType.DISCOUNT,
                description="10% off Lacoste Product",
                discount_type=enums.DiscountType.PERCENTAGE,
                discount_value=Decimal("10"),
                eligible_products=["Lacoste"]
            ),
            FreeGiftOfferOption(
                offer_type=enums.OfferType.FREE_GIFT,
                description="Free gift for 2+ items",
                min_quantity=2,
                gift_product_ids=["Prod1", "Prod2"]
            ),
            FreeShippingOfferOption(
                offer_type=enums.OfferType.FREE_SHIPPING,
                description="Free shipping for orders above $150",
                min_order_total=150
            )
        ]

    def get_offers(self, order: models.Order):
        total_discount = 0
        free_gifts = []
        free_shipping = None
        for offer in self.offers:
            if offer.offer_type == enums.OfferType.DISCOUNT:
                total_discount += offer().apply_offer(order)
            elif offer.offer_type == enums.OfferType.FREE_GIFT:
                free_gifts.extend(offer().apply_offer(order))
            elif offer.offer_type == enums.OfferType.FREE_SHIPPING and free_shipping == None:
                free_shipping = offer().apply_offer(order)

        return {
            "total_discount": total_discount,
            "free_gifts": free_gifts,
            "free_shipping": free_shipping
        }




