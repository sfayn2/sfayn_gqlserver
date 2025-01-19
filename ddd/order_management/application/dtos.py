from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import value_objects, models

class CustomerDetailsDTO(BaseModel):
    first_name: str
    last_name: str
    email: str

    def to_domain(self) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**self.dict())

class AddressDTO(BaseModel):
    street: str
    city: str
    postal: int
    country: str
    state: str

    def to_domain(self) -> value_objects.Address:
        return value_objects.Address(**self.dict())

class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str

    def to_domain(self) -> value_objects.Money:
        return value_objects.Money(**self.dict())

class PackageDTO(BaseModel):
    weight: Decimal
    dimensions: Tuple[int, int, int]

    def to_domain(self) -> value_objects.Package:
        return value_objects.Package(**self.dict())

class LineItemDTO(BaseModel):
    product_sku: str
    product_name: str 
    vendor_name: str
    product_category: str 
    options: dict
    product_price: MoneyDTO
    order_quantity: int
    package: PackageDTO
    is_free_gift: bool = False
    is_taxable: bool = True

    def to_domain(self) -> models.LineItem:
        return models.LineItem(
            product_sku=self.product_sku,
            product_name=self.product_name,
            vendor_name=self.vendor_name,
            product_category=self.product_category,
            options=self.options,
            product_price=self.product_price.to_domain(),
            order_quantity=self.order_quantity,
            package=self.package.to_domain(),
            is_free_gift=self.is_free_gift,
            is_taxable=self.is_taxable
        )



class CheckoutRequestDTO(BaseModel):
    customer_details: CustomerDetailsDTO
    address: AddressDTO
    line_items: List[LineItemDTO]

    def to_domain(self) -> models.Order:
        line_items = [item.to_domain() for item in self.line_items]
        return models.Order(
            customer_details=self.customer_details.to_domain(),
            destination=self.address.to_domain(),
            line_items=line_items
        )



class CheckoutResponseDTO(BaseModel):
    order_id: str
    order_status: str
    message: str
