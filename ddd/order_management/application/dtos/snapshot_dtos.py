import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import enums, value_objects
from ddd.order_management.application.dtos.dtos import MoneyDTO

class VendorCouponSnapshotDTO(BaseModel):
    vendor_id: uuid.UUID
    coupon_code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class VendorOfferSnapshotDTO(BaseModel):
    vendor_id: uuid.UUID
    offer_type: enums.OfferType
    name: str
    discount_value: int | Decimal
    conditions: str
    required_coupon: bool
    coupons: Optional[List[VendorCouponSnapshotDTO]]
    stackable: bool
    priority: int
    start_date: datetime
    end_date: datetime
    is_active: bool

class VendorShippingOptionSnapshotDTO(BaseModel):
    vendor_id: uuid.UUID
    name: enums.ShippingMethod
    delivery_time: str
    conditions: dict
    base_cost: MoneyDTO
    flat_rate: MoneyDTO
    currency: str
    is_active: bool

class VendorProductSnapshotDTO(BaseModel):
    product_id: uuid.UUID
    vendor_id: uuid.UUID
    product_sku: str
    product_name: str
    product_category: str
    options: dict
    product_price: MoneyDTO
    stock: int
    product_currency: str
    package_weight: Decimal
    package_length: int
    package_width: int
    package_height: int