from __future__ import annotations
from typing import Optional
from dataclasses import dataclass, field
from ddd.order_management.domain import value_objects, exceptions
from decimal import Decimal

@dataclass
class LineItem:
    product_sku: str
    product_name: str
    order_quantity: int
    vendor_id: str
    #pickup_address: value_objects.Address
    package: value_objects.Package
    product_price: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    #product_tax_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    #product_total_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())


    
    def __post_init__(self):

        if self.order_quantity <= 0:
            raise exceptions.DomainError("Order quantity must be greater than zero.")

        if self.product_price.amount < 0:
            raise exceptions.DomainError("Product price cannot be negative.")

    def __eq__(self, other):
        if not isinstance(other, LineItem):
            return False
        return self.product_sku == other.product_sku

    def __hash__(self):
        return hash(self.product_sku)
