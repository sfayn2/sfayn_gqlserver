from decimal import Decimal
from dataclasses import dataclass
from ....ordering_domain import abstract_domain_models

@dataclass(unsafe_hash=True)
class OrderItem(abstract_domain_models.Entity):
    _order_quantity: int = 1
    _product_id: str
    _product_sn: str
    _product_title: str
    _product_variant_id: str
    _product_variant_name: str
    _product_price:  Decimal
    _product_options: str
    _product_img_url = str
    _discounts_fee: Decimal

    def __post_init__(self):
        if self._order_quantity <= 0:
            raise "Invalid quantity!"

        if (self._product_price * self._order_quantity) < self._discounts_fee:
            raise "Total amount order is lower than discounts"


    def change_discount(self, discount_fee: Decimal):
        self._discount_fee  = discount_fee

    def add_order_quantity(self, order_quantity: int):
        if order_quantity < 0:
            raise "Invalid quantity!"

        self._order_quantity += order_quantity

