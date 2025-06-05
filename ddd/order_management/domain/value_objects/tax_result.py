from dataclasses import dataclass
from .money import Money
from ddd.order_management.domain import enums, exceptions

@dataclass(frozen=True) 
class TaxResult:
    desc: str
    amount: Money