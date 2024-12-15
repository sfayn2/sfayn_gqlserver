from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from enum import Enum
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
class Stock:
    _quantity: int

    def __post_init__(self):
        if not isinstance(self._quantity, int):
            raise TypeError("Stock quantity must be an integer.")
        if self._quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

    def add(self, amount: int) -> Stock:
        if amount < 0:
            raise ValueError("Cannot add a negative amount to stock.")
        return Stock(quantity=self._quantity + amount)

    def substract(self, amount: int) -> Stock:
        if amount < 0:
            raise ValueError("Cannot subtract a negative amount to stock.")
        elif amount > self._quantity:
            raise ValueError("Cannot subtract more than the availale stock.")
        return Stock(quantity=self._quantity - amount)

    def is_in_stock(self) -> bool:
        return self._quantity > 0

    def get_quantity(self):
        return self._quantity
