import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Dict, Any
from ddd.order_management.domain import enums, value_objects


class ResponseDTO(BaseModel):
    success: bool
    message: str

class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str

class ShippingOptionDTO(BaseModel):
    method: str
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
    line1: str
    city: str
    country: str
    line2: Optional[str] = None
    state: Optional[str] = None
    postal: Optional[int] = None


class PackageDTO(BaseModel):
    weight: Decimal
    dimensions: Tuple[int, int, int]

class LineItemDTO(BaseModel):
    product_sku: str
    order_quantity: int
    vendor_id: str
    pickup_address: AddressDTO
    product_price: MoneyDTO
    product_tax_amount: MoneyDTO
    product_total_amount: MoneyDTO
    package: PackageDTO


class OrderResponseDTO(BaseModel):
    order_id: str
    order_status: str
    activity_status: str
    success: bool
    message: str
    shipping_details: Optional[ShippingOptionDTO] = None
    tax_details: List[str]
    offer_details: List[str]
    tax_amount: MoneyDTO
    total_discounts_fee: MoneyDTO
    final_amount: MoneyDTO

class OrderDTO(BaseModel):
    order_id: str
    date_created: datetime 
    line_items: List[LineItemDTO]
    tracking_reference: Optional[str] = Field(json_schema_extra=AliasChoices('shipping_tracking_reference', 'tracking_reference'))
    order_status: enums.OrderStatus
    currency: str
    date_modified: Optional[datetime] = None

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

#class ShippingProvider(BaseModel):
#    provider: str
#    endpoint: str
#    api_key: str
#
#class TenantConfig(BaseModel):
#    restocking_fee_percent: Decimal
#    max_refund_amount: Decimal
#    webhook_url: str
#    shipping: ShippingProvider


class TenantDTO(BaseModel):
    tenant_id: str
    configs: Dict[str, Any]

class UserActionDTO(BaseModel):
    order_id: str
    action: str
    performed_by: str
    user_input: Dict[str, Any]

class ShipmentItemDTO(BaseModel):
    product_sku: str
    vendor_id: str
    quantity: int

# use for shipping provider
class CreateShipmentResult:
    tracking_number: str
    total_amount: MoneyDTO
    label_url: str