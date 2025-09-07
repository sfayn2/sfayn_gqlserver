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

class ShippingOptionDTO(BaseModel):
    method: enums.ShippingMethod
    delivery_time: str
    cost: MoneyDTO

    class Config:
        use_enum_values = True

class CustomerDetailsDTO(BaseModel):
    customer_id: Optional[str] = None
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

    class Config:
        use_enum_values = True

class PaymentOptionDTO(BaseModel):
    option_name: str
    method: enums.PaymentMethod
    provider: str

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
    order_stage: str
    activity_status: str
    success: bool
    message: str
    shipping_details: Optional[ShippingOptionDTO] = None
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
    customer_details: Optional[CustomerDetailsDTO] = None
    shipping_option: Optional[ShippingOptionDTO] = None
    payment_option: Optional[PaymentOptionDTO] = None
    cancellation_reason: Optional[str] = None
    total_discounts_fee: Optional[MoneyDTO] = None
    offer_details: Optional[List[str]] = None
    tax_details: Optional[List[str]] = None
    tax_amount: Optional[MoneyDTO] = None
    total_amount: Optional[MoneyDTO] = None
    final_amount: Optional[MoneyDTO] = None
    shipping_reference: Optional[str] = Field(json_schema_extra=AliasChoices('shipping_tracking_reference', 'shipping_reference'))
    coupons: Optional[List[CouponDTO]] = None
    order_stage: enums.OrderStage
    activity_status: str
    currency: str
    date_modified: Optional[datetime] = None

    class Config:
        use_enum_values = True

class OfferStrategyDTO(BaseModel):
    offer_type: enums.OfferType
    name: str
    discount_value: int | Decimal
    conditions: str
    required_coupon: bool
    coupons: Optional[List[CouponDTO]] = None
    stackable: bool
    priority: int
    start_date: datetime
    end_date: datetime
    #is_active: bool

    class Config:
        use_enum_values = True

class ShippingOptionStrategyDTO(BaseModel):
    option_name: str
    delivery_time: str
    method: enums.ShippingMethod
    conditions: dict
    base_cost: MoneyDTO
    flat_rate: MoneyDTO
    currency: str
    #is_active: bool

    class Config:
        use_enum_values = True

class ProductSkusDTO(BaseModel):
    product_sku: str
    order_quantity: int
    vendor_id: str

class UserContextDTO(BaseModel):
    sub: str
    token_type: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)


