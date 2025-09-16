from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from ddd.order_management.domain import value_objects, exceptions
from decimal import Decimal

@dataclass
class LineItem:
    product_sku: str
    product_name: str
    product_price: value_objects.Money
    order_quantity: int
    vendor: value_objects.VendorDetails
    #vendor_name: str
    product_category: str
    options: dict
    package: Optional[value_objects.Package] = None
    is_free_gift: bool = False
    is_taxable: bool = True

    
    def __post_init__(self):

        if self.order_quantity <= 0:
            raise exceptions.InvalidOrderOperation("Order quantity must be greater than zero.")

        if self.product_price.amount < 0:
            raise exceptions.InvalidOrderOperation("Product price cannot be negative.")

        if self.package and any(d <= 0 for d in self.package.dimensions):
            raise exceptions.InvalidOrderOperation("Package dimensions must be positive value.")

        ##TODO? really?
        #if self.is_free_gift and self.is_taxable:
        #    raise exceptions.InvalidOrderOperation("Free gift is not taxable.")

    @property
    def total_price(self) -> value_objects.Money:
        return self.product_price.multiply(self.order_quantity)

    @property
    def total_weight(self) -> Decimal:
        return self.package.weight * self.order_quantity

    def __eq__(self, other):
        if not isinstance(other, LineItem):
            return False
        return self.product_sku == other.product_sku and self.vendor == other.vendor

    def __hash__(self):
        return hash(self.product_sku, self.vendor)
