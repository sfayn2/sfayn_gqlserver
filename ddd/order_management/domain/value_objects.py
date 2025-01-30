from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Tuple
from decimal import Decimal, ROUND_HALF_UP
from ddd.order_management.domain import enums

@dataclass(frozen=True)
class Coupon:
    coupon_code: str

    def __post_init__(self):
        if not self.coupon_code:
            raise ValueError("Coupon code cannot be empty.")

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


    def format(self) -> Money:
        return Money(amount=Decimal(self.amount).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP), currency=self.currency)

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
    method: str
    paid_amount: Money
    transaction_id: str

    def __post_init__(self):
        if not self.method:
            raise ValueError("Payment method is required.")

        if not self.paid_amount:
            raise ValueError("Paid amount is required.")

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

    
