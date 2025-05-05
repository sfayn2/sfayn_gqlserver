from dataclasses import dataclass
from .money import Money

@dataclass(frozen=True) 
class TaxResult:
    desc: str
    amount: Money