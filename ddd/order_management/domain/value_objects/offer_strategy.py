from __future__ import annotations
import pytz
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict, Union
from datetime import datetime
from ddd.order_management.domain import enums, exceptions
from .coupon import Coupon

@dataclass(frozen=True) 
class OfferStrategy:
    offer_type: enums.OfferType
    name: str
    discount_value: int | Decimal
    conditions: dict
    required_coupon: bool
    coupons: Optional[List[Coupon]]
    stackable: bool
    priority: int
    start_date: datetime
    end_date: datetime
    is_active: bool

    def __post_init__(self):
        if not (self.is_active == True and datetime.now(pytz.utc) >= self.start_date and 
                datetime.now(pytz.utc) <= self.end_date):
            raise exceptions.OfferStrategyException(f"Offer {self.name} is no longer valid.")

        if self.offer_type == enums.OfferType.PERCENTAGE_DISCOUNT:
            if not self._is_valid_sku_list(self.conditions.get("eligible_products")):
                raise exceptions.OfferStrategyException(f"Eligible products must be a list of non-empty SKU strings.")

            if self.discount_value <= 0 or self.discount_value > 100:
                raise exceptions.OfferStrategyException("Discount value (%) must be between 0 and 100")

        if self.offer_type == enums.OfferType.FREE_GIFT:
            if  not self._is_valid_gift_products(self.conditions.get("gift_products")):
                raise exceptions.OfferStrategyException("Free gift offers must include a valid list of gift products w SKU and quantity.")
        
        if self.offer_type == enums.OfferType.FREE_SHIPPING:
            if not isinstance(self.conditions.get("minimum_order_total"), (Decimal, int)):
                raise exceptions.OfferStrategyException("Free shipping must specify a minimum order total")

    def _is_valid_sku_list(self, skus: List[str]) -> bool:
        return isinstance(skus, list) and all(isinstance(sku, str) and sku.strip() for sku in skus)

    def _is_valid_gift_products(self, gift_products: List[Dict[str, Union[str, int]]]) -> bool:
        return (
            isinstance(gift_products, list) and 
            all(
                isinstance(gp, dict) and
                isinstance(gp.get("sku"), str) and gp.get("sku").strip() != "" and 
                isinstance(gp.get("quantity"), int) and gp.get("quantity") > 0
                for gp in gift_products
            )
        )
