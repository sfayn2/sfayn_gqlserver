from __future__ import annotations
from datetime import datetime
import json
import ast
from decimal import Decimal
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from dataclasses import asdict
from typing import List, Optional, Tuple
from ddd.order_management.domain import value_objects, models, enums
from vendor_management import models as django_vendor_models

class CouponDTO(BaseModel):
    coupon_code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    #TODO: reloading coupons from db the validate is safe or correct approach?
    @staticmethod
    def from_django(coupon_code) -> CouponDTO:
        #only care on coupon code & load the rest of attrs value from db
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon_code).values().first()
        return CouponDTO(**django_coupon)

    def to_domain(self) -> value_objects.Coupon:
        from_django = django_vendor_models.Coupon.objects.filter(coupon_code=self.coupon_code).values().first()
        return value_objects.Coupon(**CouponDTO(**from_django).model_dump())

    @staticmethod
    def from_domain(coupon: value_objects.Coupon) -> CouponDTO:
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon.coupon_code).values().first()
        return CouponDTO(**django_coupon)


class CustomerDetailsDTO(BaseModel):
    first_name: str
    last_name: str
    email: str

    def to_domain(self) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**self.model_dump())


class AddressDTO(BaseModel):
    street: str
    city: str
    postal: int
    country: str
    state: str

    def to_domain(self) -> value_objects.Address:
        return value_objects.Address(**self.model_dump())

class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str

    def to_domain(self) -> value_objects.Money:
        return value_objects.Money(**self.model_dump())

class PackageDTO(BaseModel):
    weight: Decimal
    dimensions: Tuple[int, int, int]

    def to_domain(self) -> value_objects.Package:
        return value_objects.Package(**self.model_dump())

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
            options=ast.literal_eval(django_line_item.options),
            product_price=MoneyDTO(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            package=PackageDTO(
                weight=django_line_item.package_weight,
                dimensions=[django_line_item.package_length, django_line_item.package_width, django_line_item.package_height] 
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
            product_price=MoneyDTO(**asdict(line_item.product_price)),
            order_quantity=line_item.order_quantity,
            package=PackageDTO(**asdict(line_item.package)),
            is_free_gift=line_item.is_free_gift,
            is_taxable=line_item.is_taxable
        )

    def to_django(self, order: models.Order) -> dict:
        return {
                "product_sku": self.product_sku,
                "order_id": order.order_id,
                "defaults":  {
                    'product_name': self.product_name, 
                    'vendor_name': self.vendor_name, 
                    'product_category': self.product_category, 
                    'options': self.options, 
                    'product_price': self.product_price.amount, 
                    'product_currency': self.product_price.currency,
                    'order_quantity': self.order_quantity, 
                    'package_weight': self.package.weight,
                    'package_length': self.package.dimensions[0],
                    'package_width': self.package.dimensions[1],
                    'package_height': self.package.dimensions[2],
                    'is_free_gift': self.is_free_gift, 
                    'is_taxable': self.is_taxable
                }
            }

class ShippingDetailsDTO(BaseModel):
    method: enums.ShippingMethod
    delivery_time: str
    cost: MoneyDTO
    #orig_cost: MoneyDTO

    def to_domain(self) -> value_objects.ShippingDetails:
        return value_objects.ShippingDetails(
            method=self.method,
            delivery_time=self.delivery_time,
            cost=value_objects.Money(
                amount=self.cost.amount,
                currency=self.cost.currency
            )
        )

class PaymentDetailsDTO(BaseModel):
    order_id: str
    method: enums.PaymentMethod
    paid_amount: MoneyDTO
    transaction_id: str
    status: str

    def to_domain(self) -> value_objects.PaymentDetails:
        return value_objects.PaymentDetails(
            order_id=self.order_id,
            method=self.method,
            paid_amount=value_objects.Money(
                amount=self.paid_amount.amount,
                currency=self.paid_amount.currency
            ),
            transaction_id=self.transaction_id,
            status=self.status
        )

class OrderDTO(BaseModel):
    order_id: str
    date_created: datetime 
    destination: AddressDTO
    line_items: List[LineItemDTO]
    customer_details: Optional[CustomerDetailsDTO]
    shipping_details: Optional[ShippingDetailsDTO]
    payment_details: Optional[PaymentDetailsDTO]
    cancellation_reason: Optional[str]
    total_discounts_fee: Optional[MoneyDTO]
    offer_details: Optional[List[str]]
    tax_details: Optional[List[str]]
    tax_amount: Optional[MoneyDTO]
    total_amount: Optional[MoneyDTO]
    final_amount: Optional[MoneyDTO]
    shipping_reference: Optional[str] = Field(json_schema_extra=AliasChoices('shipping_tracking_reference', 'shipping_reference'))
    coupons: Optional[List[CouponDTO]]
    order_status: enums.OrderStatus
    currency: str
    date_modified: Optional[datetime]

    def to_domain(self) -> models.Order:
        line_items = [item.to_domain() for item in self.line_items]
        return models.Order(
            order_id=self.order_id,
            date_created=self.date_created,
            destination=self.destination.to_domain(),
            line_items=line_items,
            customer_details=self.customer_details.to_domain(),
            shipping_details=self.shipping_details.to_domain() if self.shipping_details else None,
            payment_details=self.payment_details.to_domain() if self.payment_details else None,
            cancellation_reason=self.cancellation_reason,
            total_discounts_fee=self.total_discounts_fee.to_domain(),
            offer_details=self.offer_details,
            tax_details=self.tax_details,
            tax_amount=self.tax_amount.to_domain(),
            total_amount=self.total_amount.to_domain(),
            final_amount=self.final_amount.to_domain(),
            shipping_reference=self.shipping_reference,
            coupons=[coupon.to_domain() for coupon in self.coupons], 
            order_status=self.order_status,
            date_modified=self.date_modified
        )

    def to_django(self):
        return {
            'order_id': self.order_id,
            'defaults': {
                    'date_created': self.date_created,
                    'delivery_street': self.destination.street,
                    'delivery_city': self.destination.city,
                    'delivery_postal': self.destination.postal,
                    'delivery_country': self.destination.country, 
                    'delivery_state': self.destination.state, 
                    'customer_first_name': self.customer_details.first_name, 
                    'customer_last_name': self.customer_details.last_name, 
                    'customer_email': self.customer_details.email if self.customer_details else None, 
                    'shipping_method': self.shipping_details.method.value if self.shipping_details else None, 
                    'shipping_delivery_time': self.shipping_details.delivery_time if self.shipping_details else None,
                    'shipping_cost': self.shipping_details.cost.amount if self.shipping_details else None,
                    'shipping_tracking_reference': self.shipping_reference,
                    'payment_method': self.payment_details.method.value if self.payment_details else None,
                    'payment_reference': self.payment_details.transaction_id if self.payment_details else None,
                    'payment_amount': self.payment_details.paid_amount.amount if self.payment_details else None, 
                    'cancellation_reason': self.cancellation_reason, 
                    'total_discounts_fee': self.total_discounts_fee.amount if self.total_discounts_fee else None, 
                    'offer_details': self.offer_details if self.offer_details else [],
                    'tax_details': self.tax_details if self.tax_details else [], 
                    'tax_amount': self.tax_amount.amount if self.tax_amount else None, 
                    'total_amount': self.total_amount.amount if self.total_amount else None, 
                    'final_amount': self.final_amount.amount if self.final_amount else None, 
                    'shipping_tracking_reference': self.shipping_reference, 
                    'coupons': [coupon.coupon_code for coupon in self.coupons], 
                    'order_status': self.order_status.value, 
                    'currency': self.currency,
                    'date_modified': self.date_modified
                }
        }
    


    @staticmethod
    def from_django_model(django_order) -> OrderDTO:
        shipping_details_dto = None
        if django_order.shipping_method:
            shipping_details_dto=ShippingDetailsDTO(
                method=django_order.shipping_method,
                delivery_time=django_order.shipping_delivery_time,
                cost=MoneyDTO(
                    amount=django_order.shipping_cost,
                    currency=django_order.currency
                )
            )

        payment_details_dto = None
        if django_order.payment_method:
            payment_details_dto=PaymentDetailsDTO(
                method=django_order.payment_method,
                transaction_id=django_order.payment_reference,
                paid_amount=MoneyDTO(
                    amount=django_order.payment_amount,
                    currency=django_order.currency
                )
            )

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
            shipping_details=shipping_details_dto if shipping_details_dto else None,
            payment_details=payment_details_dto if payment_details_dto else None,
            cancellation_reason=django_order.cancellation_reason,
            total_discounts_fee=MoneyDTO(
                amount=django_order.total_discounts_fee,
                currency=django_order.currency
            ),
            offer_details=ast.literal_eval(django_order.offer_details) if django_order.offer_details else None,
            tax_details=ast.literal_eval(django_order.tax_details) if django_order.tax_details else None,
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
            coupons=[CouponDTO.from_django(item) for item in ast.literal_eval(django_order.coupons)],
            currency=django_order.currency,
            order_status=django_order.order_status
        )

    @staticmethod
    def from_domain(order: models.Order) -> OrderDTO:
        total_discounts_fee=MoneyDTO(**asdict(order.total_discounts_fee)) if order.total_discounts_fee else None
        tax_amount=MoneyDTO(**asdict(order.tax_amount)) if order.tax_amount else None
        total_amount=MoneyDTO(**asdict(order.total_amount)) if order.total_amount else None
        final_amount=MoneyDTO(**asdict(order.final_amount)) if order.final_amount else None
        shipping_details=ShippingDetailsDTO(**asdict(order.shipping_details)) if order.shipping_details else None
        payment_details=PaymentDetailsDTO(**asdict(order.payment_details)) if order.payment_details else None
        return OrderDTO(
            order_id=order.order_id,
            destination=AddressDTO(**asdict(order.destination)),
            payment_details=payment_details,
            total_discounts_fee=total_discounts_fee,
            date_created=order.date_created,
            date_modified=order.date_modified,
            cancellation_reason=order.cancellation_reason,
            offer_details=order.offer_details,
            tax_details=order.tax_details,
            shipping_details=shipping_details,
            tax_amount=tax_amount,
            total_amount=total_amount,
            final_amount=final_amount,
            shipping_reference=order.shipping_reference,
            coupons=[CouponDTO.from_domain(item) for item in order.coupons],
            order_status=order.order_status,
            customer_details=CustomerDetailsDTO(**asdict(order.customer_details)),
            line_items=[
                LineItemDTO.from_domain(item) for item in order.line_items
            ],
            currency=order.currency
        )



class OfferStrategyDTO(BaseModel):
    offer_type: enums.OfferType
    name: str
    discount_value: int | Decimal
    conditions: str
    required_coupon: bool
    coupons: Optional[List[CouponDTO]]
    stackable: bool
    priority: int
    start_date: datetime
    end_date: datetime
    is_active: bool

    def to_domain(self) -> value_objects.OfferStrategy:

        #first coupon is invalid and second is valid should not stop processing Offer, hence, skipping error
        coupons = []
        for item in self.coupons:
            try:
                coupons.append(item.to_domain())
            except:
                #TODO: add logger
                continue

        return value_objects.OfferStrategy(
            **self.model_dump(exclude={"coupons", "conditions"}),
            conditions=ast.literal_eval(self.conditions),
            coupons=coupons
        )

