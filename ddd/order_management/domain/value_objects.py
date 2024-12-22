from __future__ import annotations
from dataclasses import dataclass
from typing import Union
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
class OrderLine:
    _product_sku: str
    _options: str
    _product_price: Money
    _order_quantity: int
    _total_price = Money

    def get_total_price(self) -> Money:
        return self._total_price.multiply(self._order_quantity)


@dataclass(frozen=True)
class Address:
    _address: str
    _city: str
    _postal: int
    _country: str

@dataclass(frozen=True)
class Payment:
    _method: str
    _amount: Money

    def get_amount(self):
        return self._amount

