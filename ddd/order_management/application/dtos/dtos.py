import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Dict, Any
from ddd.order_management.domain import enums, value_objects



class MoneyDTO(BaseModel):
    amount: Decimal
    currency: str

class ShipmentItemDTO(BaseModel):
    product_sku: str
    vendor_id: str
    quantity: int

class CustomerDetailsDTO(BaseModel):
    customer_id: Optional[str] = None
    name: str
    email: str

class AddressDTO(BaseModel):
    line1: str
    city: str
    country: str
    line2: Optional[str] = None
    state: Optional[str] = None
    postal: Optional[int] = None


class PackageDTO(BaseModel):
    weight_kg: Decimal
    #dimensions: Tuple[int, int, int]

class LineItemDTO(BaseModel):
    product_sku: str
    product_name: str
    order_quantity: int
    vendor_id: str
    #pickup_address: AddressDTO
    product_price: MoneyDTO
    package: PackageDTO



class OrderDTO(BaseModel):
    tenant_id: str
    customer_details: CustomerDetailsDTO
    order_id: str
    currency: str
    order_status: enums.OrderStatus
    payment_status: enums.PaymentStatus
    line_items: List[LineItemDTO]
    shipments: List[ShipmentItemDTO]
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None

    class Config:
        use_enum_values = True


class ProductSkusDTO(BaseModel):
    product_sku: str
    order_quantity: int
    vendor_id: str
    product_name: str
    product_price: MoneyDTO
    package: PackageDTO

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



class ConfirmShipmentDTO(BaseModel):
    tenant_id: str
    order_id: str
    shipment_id: str
    order_status: enums.OrderStatus

class AddOrderDTO(BaseModel):
    external_ref: str
    tenant_id: str
    customer_details: CustomerDetailsDTO
    product_skus: List[ProductSkusDTO]

class ShippingWebhookDTO(BaseModel):
    provider: str
    tracking_reference: str
    tenant_id: str
    status: str
    occured_at: datetime
    raw_payload: dict


# SaasConfig / TenantConfig related DTOs
class CreateShipmentConfigDTO(BaseModel):
    # all shipments tracker webhook / create shipments
    provider: str
    api_key: str
    endpoint: str

class WebhookReceiverConfigDTO(BaseModel):
    provider: str
    shared_secret: str
    max_age_seconds: Optional[int] = None
