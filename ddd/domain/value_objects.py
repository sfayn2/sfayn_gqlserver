from dataclasses import dataclass
from enum import Enum

class Currency(Enum):
    USD = "USD"
    SGD = "SGD"

@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies!")
        
        return Money(self.amount + other.amount)