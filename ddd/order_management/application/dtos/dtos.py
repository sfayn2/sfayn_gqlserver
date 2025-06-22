import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import enums, value_objects


class ResponseDTO(BaseModel):
    success: bool
    message: str

class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str

class ShippingDetailsDTO(BaseModel):
    method: enums.ShippingMethod
    delivery_time: str
    cost: MoneyDTO

    class Config:
        use_enum_values = True

class CustomerDetailsDTO(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str

class AddressDTO(BaseModel):
    street: str
    city: str
    postal: int
    country: str
    state: str

class VendorDetailsDTO(BaseModel):
    vendor_id: str
    name: Optional[str] = None
    country: Optional[str] = None

class PackageDTO(BaseModel):
    weight: Decimal
    dimensions: Tuple[int, int, int]

class PaymentDetailsDTO(BaseModel):
    order_id: str
    method: enums.PaymentMethod
    paid_amount: MoneyDTO
    transaction_id: str
    status: enums.PaymentStatus

class LineItemDTO(BaseModel):
    product_sku: str
    product_name: str 
    vendor: VendorDetailsDTO
    product_category: str 
    options: dict
    product_price: MoneyDTO
    order_quantity: int
    package: PackageDTO
    is_free_gift: bool = False
    is_taxable: bool = True


class OrderResponseDTO(BaseModel):
    order_id: str
    order_status: str
    success: bool
    message: str
    shipping_details: Optional[ShippingDetailsDTO]
    tax_details: List[str]
    offer_details: List[str]
    tax_amount: MoneyDTO
    total_discounts_fee: MoneyDTO
    final_amount: MoneyDTO

class CouponDTO(BaseModel):
    coupon_code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

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

class ShippingOptionStrategyDTO(BaseModel):
    name: enums.ShippingMethod
    delivery_time: str
    conditions: dict
    base_cost: MoneyDTO
    flat_rate: MoneyDTO
    currency: str
    is_active: bool

class ProductSkusDTO(BaseModel):
    product_sku: str
    order_quantity: int
