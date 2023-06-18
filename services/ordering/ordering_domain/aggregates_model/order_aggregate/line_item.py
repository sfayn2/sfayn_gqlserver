from decimal import Decimal
from dataclasses import dataclass
from ....ordering_domain import abstract_domain_models
from .money import Money

@dataclass(unsafe_hash=True)
class LineItem(abstract_domain_models.Entity):
    _product_id: str
    _sku: str #TODO valueobject?
    _quantity: int = 1
    _price:  Money
    _discounts: Money

    def __post_init__(self):
        if self._quantity <= 0:
            raise "Invalid quantity!"

        if (self._price * self._quantity) < self._discounts:
            raise "Total amount order is lower than discounts"


    def change_discount(self, discount_fee: Money):
        self._discounts  = discount_fee

    def add_quantity(self, quantity: int):
        if quantity < 0:
            raise "Invalid quantity!"

        self._quantity += quantity

