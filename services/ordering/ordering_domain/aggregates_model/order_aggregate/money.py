
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from ....ordering_domain import abstract_domain_models

class Currency(StrEnum):
    USD = "USD"
    SGD = "SGD"


@dataclass(frozen=True)
class Money(abstract_domain_models.ValueObject):
    value: Decimal
    currency: Currency

    def add(self, other: Decimal) -> Money:
        if other.value < 0:
            raise "Invalid amount!"

        if self.currency != other.currency:
            raise "Invalid currency!"

        return Money(self.value + other.value, self.currency)

    def multiply(self, other: Decimal) -> Money:
        if other.value < 0:
            raise "Invalid amount!"

        if self.currency != other.currency:
            raise "Invalid currency!"

        return Money(self.value * other.value, self.currency)