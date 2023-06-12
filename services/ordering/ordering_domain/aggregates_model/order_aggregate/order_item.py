from decimal import Decimal
from ....ordering_domain import abstract_domain_models

class OrderItem(abstract_domain_models.Entity):

    def __init__(
        self
        order_quantity: int = 1,
        product_id: str,
        product_sn: str,
        product_title: str,
        product_variant_id: str,
        product_variant_name: str,
        product_price:  Decimal,
        product_options: str,
        product_img_url = str,
        discounts_fee: Decimal,
    ):
        if self.order_quantity <= 0:
            raise "Invalid quantity!"

        if (self.product_price * self.order_quantity) < self.discounts_fee:
            raise "Total amount order is lower than discounts"

        self._add_order_quantity = order_quantity
        self._product_id = product_id
        self._product_sn = product_sn
        self._product_title = product_title
        self._product_variant_id = product_variant_id
        self._product_variant_name = product_variant_name
        self._product_price = product_price
        self._product_options = product_options
        self._product_img_url = product_img_url
        self._discounts_fee = discounts_fee

    def change_discount(self, discount_fee: Decimal):
        self._discount_fee  = discount_fee

    def add_order_quantity(self, order_quantity: int):
        if order_quantity < 0:
            raise "Invalid quantity!"

        self._order_quantity += order_quantity

