from decimal import Decimal
from dataclasses import dataclass
from ....ordering_domain import abstract_domain_models
from .money import Money


@dataclass(frozen=True)
class DeliveryAddress(abstract_domain_models.ValueObject):
    address:  str
    postal:  int
    country:  str
    region:  str

    def __post_init__(self):
        if self.address is None:
            raise "Invalid address value!"

        if self.postal is None:
            raise "Invalid postal value!"

        if self.country is None:
            raise "Invalid country value!"

        if self.region is None:
            raise "Invalid region value!"


@dataclass(unsafe_hash=True)
class LineItem(abstract_domain_models.Entity):
    _item_sku: str #TODO valueobject?
    _item_quantity: int = 1
    _item_price:  Money
    _item_discounts_fee: Money
    _item_delivery_address: DeliveryAddress

    def __post_init__(self):
        if self._item_quantity <= 0:
            raise "Invalid quantity!"

        if (self._item_price * self._item_quantity) < self._item_discounts_fee:
            raise "Total amount order is lower than discounts"
    
    def as_dict(self):
        return {
            "order_quantity": self._item_quantity,
            "product_variant":  self._item_sku,
            "product_price": self._item_price,
            "discounts_fee": self._item_discounts_fee,
            "discounted_price": self.get_item_discounted_price(),
            "total": self.get_item_total()
        }

    def add_quantity(self, quantity: int):
        if quantity < 0:
            raise "Invalid quantity!"

        self._quantity += quantity

    def minus_quantity(self, quantity: int):
        if quantity < 0 or quantity > self._quantity:
            raise "Invalid quantity!"

        self._quantity -= quantity

    def get_item_discounted_price(self):
        return (self._item_price * self._item_quantity) - self._item_discounts_fee

    def get_item_total(self):
        if self._item_discounts_fee:
            return self.get_item_discounted_price()
        else:
            return (self._item_price * self._item_quantity)


