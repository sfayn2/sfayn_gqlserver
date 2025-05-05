from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from decimal import Decimal

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

