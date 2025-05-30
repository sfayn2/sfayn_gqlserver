from dataclasses import dataclass, field
from ddd.order_management.domain import models

@dataclass(frozen=True) 
class OfferResult:
    name: str
    desc: str
    discounts_fee: Money = field(default_factory=lambda: Money.default())
    free_gifts: List[models.LineItem] = field(default_factory=list)
    free_shipping: bool = False