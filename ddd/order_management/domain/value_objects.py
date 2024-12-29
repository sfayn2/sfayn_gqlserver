from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Tuple
from decimal import Decimal
from ddd.order_management.domain import enums

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            raise TypeError("Amount must be a decimal.")
        if not isinstance(self.currency, str):
            raise TypeError("Currency must be a string.")
        if self.amount <= Decimal(0):
            raise ValueError(f"Amount must be non zero.")

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


@dataclass(frozen=True)
class LineItem:
    _product_sku: str
    _product_name: str
    _options: str
    _product_price: Money
    _order_quantity: int
    is_free_gift: bool = False
    is_taxable: bool = True
    package: Package
    _discounts_fee: Money

    #below not applicable? getter is enough?
    #_discounted_price: Money
    #_total_price = Money -> not applicable?

    def add(self, quantity: int):
        if quantity < 0:
            raise ValueError("Value must be greater than current quantity.")

        self._order_quantity += quantity

    def subtract(self, quantity: int):
        if quantity < 0 or quantity > self._order_quantity:
            raise ValueError("Value must be less than or equal to the current quantity.")

        self._order_quantity -= quantity

    def set_discounts_fee(self, amount: Money):
        self._discounts_fee = amount

    def get_total_price(self) -> Money:
        #if self._discounts_fee:
        #    return self.get_discounted_price()
        #else:
        #    return (self._product_price * self._order_quantity)
        return (self._product_price * self._order_quantity)

    #def get_discounted_price(self):
    #    return (self._product_price * self._order_quantity) - self._discounts_fee

    def get_total_weight(self) -> Decimal:
        return self._weight * self._order_quantity

    def get_product_name(self):
        return self._product_name

    def get_order_quantity(self):
        return self._order_quantity



@dataclass(frozen=True)
class Address:
    _address: str
    _city: str
    _postal: int
    _country: str
    _state: str
    # make use of country to country code converter if require?

    def is_international(self, origin_country: str) -> bool:
        return self._country != origin_country

    def get_state(self):
        return self._state

    def get_country(self):
        return self._country

class Package:
    _weight: Decimal #in kg
    _dimensions: Tuple[int, int, int] # (length, width, height) in cm

    def get_weight(self):
        return self._weight

    def get_dimensions(self):
        return self._dimensions

@dataclass(frozen=True)
class Payment:
    method: str
    paid_amount: Money


#right now only for Gues customer
@dataclass(frozen=True)    
class Customer:
    _first_name: str
    _last_name: str
    _email: str

@dataclass(frozen=True)
class ShippingDetails:
    method: enums.ShippingMethod
    delivery_time: str
    cost: Money

    def __post_init__(self):
        if not self.method.strip():
            raise ValueError("Shipping method is required.")

@dataclass(frozen=True)
class TaxDetails:
    desc: str
    tax_amount: Money
    
