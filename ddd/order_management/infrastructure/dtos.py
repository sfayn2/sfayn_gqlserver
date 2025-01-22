import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import List, Optional, Tuple
from ddd.order_management.domain import value_objects, models, enums

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

class ShippingDetailsDTO(BaseModel):
    method: enums.ShippingMethod
    delivery_time: str
    cost: MoneyDTO
    orig_cost: MoneyDTO

    def to_domain(self) -> value_objects.ShippingDetails:
        return value_objects.ShippingDetails(**self.dict())

class PaymentDetailsDTO(BaseModel):
    method: str
    paid_amount: MoneyDTO
    transaction_id: str

    def to_domain(self) -> value_objects.PaymentDetails:
        return value_objects.PaymentDetails(**self.dict())

class OrderDTO(BaseModel):
    order_id: str
    date_created: datetime 
    destination: AddressDTO
    line_items: List[LineItemDTO]
    customer_details: CustomerDetailsDTO
    shipping_details: ShippingDetailsDTO
    payment_details: PaymentDetailsDTO
    cancellation_reason: str
    total_discounts_fee: MoneyDTO
    offer_details: str
    tax_details: str
    tax_amount: MoneyDTO
    total_amount: MoneyDTO
    final_amount: MoneyDTO
    shipping_reference: str
    coupon_codes: List[str]
    status: enums.OrderStatus
    date_modified: datetime

    def to_domain(self) -> models.Order:
        line_items = [item.to_domain() for item in self.line_items]
        return models.Order(
            order_id=self.order_id,
            date_created=self.date_created,
            destination=self.address.to_domain(),
            line_items=line_items,
            customer_details=self.customer_details.to_domain(),
            shipping_details=self.shipping_details.to_domain(),
            payment_details=self.payment_details.to_domain(),
            cancellation_reason=self.cancellation_reason,
            total_discounts_fee=self.total_discounts_fee.to_domain(),
            offer_details=self.offer_details,
            tax_details=self.tax_details,
            tax_amount=self.tax_amount.to_domain(),
            total_amount=self.total_amount.to_domain(),
            final_amount=self.final_amount.to_domain(),
            shipping_reference=self.shipping_reference,
            coupon_codes=[coupon for coupon in self.coupon_codes],
            status=self.status,
            date_modified=self.date_modified
        )

    def to_django_defaults(self):
        return self.dict(exclude={"order_id", "line_items"})
