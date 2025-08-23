import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import enums, value_objects
from ddd.order_management.application.dtos.dtos import MoneyDTO

class VendorDetailsSnapshotDTO(BaseModel):
    vendor_id: str
    tenant_id: str
    name: str
    country: str
    is_active: bool

class VendorCouponSnapshotDTO(BaseModel):
    vendor_id: str
    tenant_id: str
    offer_id: str
    coupon_code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class VendorOfferSnapshotDTO(BaseModel):
    tenant_id: str
    vendor_id: str
    offer_id: str
    offer_type: enums.OfferType
    name: str
    discount_value: int | Decimal
    conditions: dict
    required_coupon: bool
    stackable: bool
    priority: int
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        use_enum_values = True

class VendorShippingOptionSnapshotDTO(BaseModel):
    tenant_id: str
    vendor_id: str
    option_name: str
    method: enums.ShippingMethod
    provider: str
    delivery_time: str
    conditions: dict
    base_cost: Decimal
    flat_rate: Decimal
    currency: str
    is_active: bool

    class Config:
        use_enum_values = True

class VendorProductSnapshotDTO(BaseModel):
    product_id: str
    tenant_id: str
    vendor_id: str
    product_sku: str
    product_name: str
    product_category: str
    options: dict
    product_price: Decimal
    stock: int
    product_currency: str
    #package_weight: Decimal = Field(alias="package_weight_kg")
    #package_length: int = Field(alias="package_length_cm")
    #package_width: int = Field(alias="package_width_cm")
    #package_height: int = Field(alias="package_height_cm")
    package_weight: Decimal
    package_length: int
    package_width: int
    package_height: int
    is_active: bool

class CustomerDetailsSnapshotDTO(BaseModel):
    customer_id: str
    user_id: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    is_active: bool

class CustomerAddressSnapshotDTO(BaseModel):
    customer_id: str
    address_type: str
    street: str
    city: str
    state: str
    postal: int
    country: str
    is_default: bool
    is_active: bool

