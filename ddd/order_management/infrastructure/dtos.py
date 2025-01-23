from __future__ import annotations
from datetime import datetime
import json
from decimal import Decimal
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
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

    @staticmethod
    def from_django_model(django_line_item) -> LineItemDTO:
        return LineItemDTO(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            vendor_name=django_line_item.vendor_name,
            product_category=django_line_item.product_category,
            options=json.loads(django_line_item.options),
            product_price=MoneyDTO(
                amount=django_line_item.product_price,
                currency=django_line_item.currency
            ),
            order_quantity=django_line_item.order_quantity,
            package=PackageDTO(
                weight=django_line_item.weight,
                dimensions=[django_line_item.length, django_line_item.width, django_line_item.height] 
            ),
            is_free_gift=django_line_item.is_free_gift,
            is_taxable=django_line_item.is_taxable
        )

    @staticmethod
    def from_domain(line_item: models.LineItem) -> LineItemDTO:
        return LineItemDTO(
            product_sku=line_item.product_sku,
            product_name=line_item.product_name,
            vendor_name=line_item.vendor_name,
            product_category=line_item.product_category,
            options=line_item.options,
            product_price=MoneyDTO(
                amount=line_item.product_price,
                currency=line_item.currency
            ),
            order_quantity=line_item.order_quantity,
            package=PackageDTO(line_item.package),
            is_free_gift=line_item.is_free_gift,
            is_taxable=line_item.is_taxable
        )

    def to_django_defaults(self, order: models.Order) -> dict:
        return self.dict().update({"order_id": order.order_id})

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
    shipping_reference: str = Field(json_schema_extra=AliasChoices('shipping_tracking_reference', 'shipping_reference'))
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

    @staticmethod
    def from_django_model(django_order) -> OrderDTO:
        return OrderDTO(
            order_id=django_order.order_id,
            date_created=django_order.date_created,
            date_modified=django_order.date_modified, 
            destination=AddressDTO(
                street=django_order.delivery_street,
                city=django_order.delivery_city,
                postal=django_order.delivery_postal,
                country=django_order.delivery_country,
                state=django_order.delivery_state
            ),
            line_items=[
                LineItemDTO.from_django_model(item) for item in django_order.line_items.all()
            ],
            customer_details=CustomerDetailsDTO(
                first_name=django_order.customer_first_name,
                last_name=django_order.customer_last_name,
                email=django_order.customer_email
            ),
            shipping_details=ShippingDetailsDTO(
                method=django_order.shipping_method,
                delivery_time=django_order.shipping_delivery_time,
                cost=MoneyDTO(
                    amount=django_order.shipping_cost,
                    currency=django_order.currency
                ),
                orig_cost=MoneyDTO(
                    amount=django_order.shipping_cost,
                    currency=django_order.currency
                ),
            ),
            payment_details=PaymentDetailsDTO(
                method=django_order.payment_method,
                transaction_id=django_order.payment_reference,
                paid_amount=MoneyDTO(
                    amount=django_order.payment_amount,
                    currency=django_order.currency
                )
            ),
            cancellation_reason=django_order.cancellation_reason,
            total_discounts_fee=MoneyDTO(
                amount=django_order.total_discounts_fee,
                currency=django_order.currency
            ),
            offer_details=django_order.offer_details,
            tax_details=django_order.tax_details,
            tax_amount=MoneyDTO(
                amount=django_order.tax_amount,
                currency=django_order.currency
            ),
            total_amount=MoneyDTO(
                amount=django_order.total_amount,
                currency=django_order.currency
            ),
            final_amount=MoneyDTO(
                amount=django_order.final_amount,
                currency=django_order.currency
            ),
            shipping_reference=django_order.shipping_tracking_reference,
            coupon_codes=django_order.coupon_codes,
            status=django_order.status
        )

    @staticmethod
    def from_domain(order: models.Order) -> OrderDTO:
        return OrderDTO(
            **order.__dict__,
            destination=AddressDTO(order.destination),
            line_items=parse_obj_as(List[LineItemDTO], order.line_items),
            customer_details=CustomerDetailsDTO(order.customer_details),
            shipping_details=ShippingDetailsDTO(order.shipping_details),
            payment_details=PaymentDetailsDTO(order.payment_details),
        )

