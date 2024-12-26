from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Tuple
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    _amount: Decimal
    _currency: str

    def __post_init__(self):
        if not isinstance(self._amount, Decimal):
            raise TypeError("Amount must be a decimal.")
        if not isinstance(self._currency, str):
            raise TypeError("Currency must be a string.")
        if self._amount <= Decimal(0):
            raise ValueError(f"Amount must be non zero.")

        if len(self._currency) != 3:
            raise ValueError("Currency must be a valid 3 character ISO code.")

    def add(self, other: Money) -> Money:
        if self._currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(amount=self._amount + other.amount, currency=self._currency)

    def subtract(self, other: Money) -> Money:
        if self._currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(amount=self._amount - other.amount, currency=self._currency)

    def multiply(self, multiplier: Union[int, Decimal]) -> Money:
        return Money(amount=self._amount * Decimal(multiplier), currency=self._currency)

    def divide(self, divisor: Union[int, Decimal]) -> Money:
        return Money(amount=self._amount / Decimal(divisor), currency=self._currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._amount == other.amount and self._currency == other.currency
    
    def get_amount(self):
        return self._amount

@dataclass(frozen=True)
class LineItem:
    _product_sku: str
    _product_name: str
    _options: str
    _product_price: Money
    _order_quantity: int
    _discounts_fee: Money
    package: Package
    #_total_price = Money

    def get_total_price(self) -> Money:
        if self._discounts_fee:
            return self.get_discounted_price()
        else:
            return (self._product_price * self._order_quantity)

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

    def get_discounted_price(self):
        return (self._product_price * self._order_quantity) - self._discounts_fee

    def get_total_weight(self) -> Decimal:
        return self._weight * self._order_quantity

    #def total_volume(self) -> int:
    #    length, width, height = self.package.get_dimensions()
    #    return length*width*height*self._order_quantity

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

    def is_international(self, origin_country: str) -> bool:
        return self._country != origin_country

class Package:
    _weight: Decimal #in kg
    _dimensions: Tuple[int, int, int] # (length, width, height) in cm

    def get_weight(self):
        return self._weight

    def get_dimensions(self):
        return self._dimensions

@dataclass(frozen=True)
class Payment:
    _method: str
    _amount: Money

    def get_amount(self):
        return self._amount



