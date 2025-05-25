from dataclasses import dataclass
from ddd.order_management.domain import value_objects
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
    package: value_objects.Package
    is_free_gift: bool = False
    is_taxable: bool = True

    
    def __post_init__(self):

        if self.order_quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        if self.product_price.amount < 0:
            raise ValueError("Product price cannot be negative.")

        if any(d <= 0 for d in self.package.dimensions):
            raise ValueError("Package dimensions must be positive value.")

        #TODO? really?
        if self.is_free_gift and self.is_taxable:
            raise ValueError("Free gift is not taxable.")

    def update_order_quantity(self, new_quantity: int):
        if new_quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        self.order_quantity = new_quantity

    @property
    def total_price(self) -> value_objects.Money:
        return self.product_price.multiply(self.order_quantity)

    @property
    def total_weight(self) -> Decimal:
        return self.package.weight * self.order_quantity

    def __eq__(self, other):
        if not isintance(other, LineItem):
            return False
        return self.product_sku == other.product_sku and self.vendor == other.vendor

    def __hash__(self):
        return hash(self.product_sku, self.vendor)
