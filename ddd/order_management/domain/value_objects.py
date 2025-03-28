from __future__ import annotations
import pytz
from datetime import datetime
from dataclasses import dataclass
from typing import Union, Tuple, Optional, List, Dict
from decimal import Decimal, ROUND_HALF_UP
from ddd.order_management.domain import enums, exceptions

@dataclass(frozen=True)
class Coupon:
    coupon_code: str
    start_date: datetime
    end_date: datetime
    is_active: bool

    def __post_init__(self):
        if not self.coupon_code:
            raise ValueError("Coupon code cannot be empty.")

        if not (self.is_active and datetime.now(pytz.utc) >= self.start_date and datetime.now(pytz.utc) <= self.end_date):
            raise ValueError(f"Coupon code {self.coupon_code} no longer valid.")



@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            raise TypeError("Amount must be a decimal.")
        if not isinstance(self.currency, str):
            raise TypeError("Currency must be a string.")

        if self.amount < Decimal("0"):
            raise ValueError(f"Amount must not be negative.")

        if len(self.currency) != 3:
            raise ValueError("Currency must be a valid 3 character ISO code.")


    #def format(self) -> Money:
    #    return Money(amount=Decimal(self.amount).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP), currency=self.currency)

    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def multiply(self, multiplier: Union[int, Decimal]) -> Money:
        return Money(amount=self.amount * Decimal(multiplier), currency=self.currency)

    def divide(self, divisor: Union[int, Decimal]) -> Money:
        return Money(amount=self.amount / Decimal(divisor), currency=self.currency)

    def reset_amount(self) -> Money:
        return Money(amount=Decimal("0"), currency=self.currency)

    @classmethod
    def default(cls) -> Money:
        return Money(amount=Decimal("0"), currency="SGD") #need to get from settigns?



@dataclass(frozen=True)
class Address:
    street: str
    city: str
    postal: int
    country: str
    state: str
    # make use of country to country code converter if require?

    def __post_init__(self):
        if not self.street or not self.city or not self.postal or not self.state:
            raise ValueError("Address fields (street, city, postal, country, state) cannot be empty.")
        if not isinstance(self.postal, int) or self.postal <= 0:
            raise ValueError(f"Invalid postal code {self.postal}. It must be a positive integer.")
        #TODO: validate country & state?

    def is_international(self, origin_country: str) -> bool:
        return self.country != origin_country


@dataclass(frozen=True)
class Package:
    weight: Decimal #in kg
    #weight_unit: str = "kg"
    dimensions: Tuple[int, int, int] # (length, width, height) in cm
    #dimensions_unit: str = "cm"

    def __post_init__(self):
        if self.weight <= Decimal("0"):
            raise ValueError("Weight must be greater than zero.")
        if not isinstance(self.dimensions, tuple) and len(self.dimensions) == 3:
            raise TypeError("Dimensions must be a tuple of length 3 (length, width, height)")
        if any(d <= 0 for d in self.dimensions):
            raise ValueError("All dimensions must be greater than zero.")


@dataclass(frozen=True)
class PaymentDetails:
    order_id: str
    method: str
    paid_amount: Money
    transaction_id: str
    status: str

    def __post_init__(self):
        if not self.order_id:
            raise ValueError("Order Id in is required for 3rd Party payment verification.")

        if not self.method:
            raise ValueError("Payment method is required.")

        if not self.paid_amount:
            raise ValueError("Paid amount is required.")

        if not self.status:
            raise ValueError("Payment status is required.")

        if not self.method.value in [item.value for item in enums.PaymentMethod]:
            raise ValueError(f"Payment method {self.method.value} not supported.")

        if self.paid_amount and self.paid_amount.amount < Decimal("0"):
            raise ValueError("Paid amount cannot be negative.")

        if not self.method != enums.PaymentMethod.COD and not self.transaction_id:
            raise ValueError("Transaction ID is required for non-COD payments.")


#right now only for Gues customer
@dataclass(frozen=True)    
class CustomerDetails:
    first_name: str
    last_name: str
    email: str

    def __post_init__(self):
        if not self.first_name or not self.last_name or not self.email:
            raise ValueError("Customer details are incomplete.")
        #TODO: validate email

@dataclass(frozen=True)
class ShippingDetails:
    #customer shipping option
    method: enums.ShippingMethod

    delivery_time: str
    cost: Money
    #orig_cost: Money

    def __post_init__(self):
        if not self.method:
            raise ValueError("Shipping method is required.")

        if not self.cost:
            raise ValueError("Shipping cost is required.")

        if not self.delivery_time:
            raise ValueError("Delivery time is required.")

        if not self.method.value in [item.value for item in enums.ShippingMethod]:
            raise ValueError(f"Shipping method {self.method.value} not supported.")

        if self.cost and self.cost.amount < Decimal("0"):
            raise ValueError("Shipping cost cannot be negative.")

        
    #make use of order.update_shipping_details to take effect
    #def reset_cost(self):
    #    return ShippingDetails(method=self.method, 
    #                           delivery_time=self.delivery_time, 
    #                           cost=self.orig_cost, 
    #                           orig_cost=self.orig_cost
    #                        )

    #make use of order.update_shipping_details to take effect
    def update_cost(self, new_cost: Money):
        return ShippingDetails(method=self.method, 
                               delivery_time=self.delivery_time, 
                               cost=new_cost
                            )

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
            raise exceptions.InvalidOfferOperation(f"Offer {self.name} is no longer valid.")

        if self.offer_type == enums.OfferType.PERCENTAGE_DISCOUNT:
            if not self._is_valid_sku_list(self.conditions.get("eligible_products")):
                raise exceptions.InvalidOfferOperation(f"Eligible products must be a list of non-empty SKU strings.")

            if self.discount_value <= 0 or self.discount_value > 100:
                raise exceptions.InvalidOfferOperation("Discount value (%) must be between 0 and 100")

        if self.offer_type == enums.OfferType.FREE_GIFT:
            if  not self._is_valid_gift_products(self.conditions.get("gift_products")):
                raise exceptions.InvalidOfferOperation("Free gift offers must include a valid list of gift products w SKU and quantity.")
        
        if self.offer_type == enums.OfferType.FREE_SHIPPING:
            if not isinstance(self.conditions.get("minimum_order_total"), (Decimal, int)):
                raise exceptions.InvalidOfferOperation("Free shipping must specify a minimum order total")

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


@dataclass(frozen=True) 
class TaxResult:
    desc: str
    amount: Money

@dataclass(frozen=True) 
class VendorDetails:
    name: str
    country: str


@dataclass(frozen=True) 
class ShippingOptionStrategy:
    name: enums.ShippingMethod
    delivery_time: str
    conditions: dict
    base_cost: Money
    flat_rate: Money
    is_active: bool