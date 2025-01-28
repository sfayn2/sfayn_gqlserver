from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Tuple
from decimal import Decimal
from ddd.order_management.domain import enums

@dataclass(frozen=True)
class Coupon:
    coupon_code: str

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
        return Money(amount=Decimal("0"), currency="TBD") #need to get from settigns?



@dataclass(frozen=True)
class Address:
    street: str
    city: str
    postal: int
    country: str
    state: str
    # make use of country to country code converter if require?

    def is_international(self, origin_country: str) -> bool:
        return self.country != origin_country


@dataclass(frozen=True)
class Package:
    weight: Decimal #in kg
    dimensions: Tuple[int, int, int] # (length, width, height) in cm


@dataclass(frozen=True)
class PaymentDetails:
    method: str
    paid_amount: Money
    transaction_id: str


#right now only for Gues customer
@dataclass(frozen=True)    
class CustomerDetails:
    first_name: str
    last_name: str
    email: str

@dataclass(frozen=True)
class ShippingDetails:
    method: enums.ShippingMethod
    delivery_time: str
    cost: Money
    #orig_cost: Money

    def __post_init__(self):
        if not self.method:
            raise ValueError("Shipping method is required.")
        
    #make use of order.update_shipping_details to take effect
    def reset_cost(self):
        return ShippingDetails(method=self.method, 
                               delivery_time=self.delivery_time, 
                               cost=self.orig_cost, 
                               orig_cost=self.orig_cost
                            )

    #make use of order.update_shipping_details to take effect
    def update_cost(self, new_cost: Money):
        return ShippingDetails(method=self.method, 
                               delivery_time=self.delivery_time, 
                               cost=new_cost
                            )

    
