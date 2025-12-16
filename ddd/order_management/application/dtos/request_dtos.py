from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from ddd.order_management.domain import enums

# define security context
class RequestContextDTO(BaseModel):
    token: str
    tenant_id: str

class MoneyRequestDTO(BaseModel):
    amount: Decimal
    currency: str


class CustomerDetailsRequestDTO(BaseModel):
    customer_id: Optional[str] = None
    name: str
    email: str

class AddressRequestDTO(BaseModel):
    line1: str
    city: str
    country: str
    line2: Optional[str] = None
    state: Optional[str] = None
    postal: Optional[str] = None


class PackageRequestDTO(BaseModel):
    weight_kg: Decimal
    #dimensions: Tuple[int, int, int]

class LineItemRequestDTO(BaseModel):
    product_sku: str
    product_name: str
    order_quantity: int
    vendor_id: str
    #pickup_address: AddressRequestDTO
    product_price: MoneyRequestDTO
    package: PackageRequestDTO

class ShipmentItemRequestDTO(BaseModel):
    product_sku: str
    quantity: int
    vendor_id : str

class ShipmentRequestDTO(BaseModel):
    shipment_id: Optional[str] = None
    shipment_address: Optional[AddressRequestDTO] = None
    shipment_provider: Optional[str] = None
    # Use the actual enum class from your domain models
    shipment_mode: Optional[enums.ShipmentMethod] = None

    # package details
    package_weight_kg: Optional[Decimal] = None
    package_length_cm: Optional[Decimal] = None
    package_width_cm: Optional[Decimal] = None
    package_height_cm: Optional[Decimal] = None

    # pickup mode details
    pickup_address: Optional[AddressRequestDTO] = None
    pickup_window_start: Optional[datetime] = None # Maps to graphene.DateTime
    pickup_window_end: Optional[datetime] = None
    pickup_instructions: Optional[str] = None

    tracking_reference: Optional[str] = None
    label_url: Optional[str] = None
    shipment_amount: Optional[MoneyRequestDTO] = None
    # Use the actual enum class from your domain models
    shipment_status: Optional[enums.ShipmentStatus] = None 
    shipment_items: Optional[List[ShipmentItemRequestDTO]] = None

class ProductSkusRequestDTO(BaseModel):
    product_sku: str
    order_quantity: int
    vendor_id: str
    product_name: str
    product_price: MoneyRequestDTO
    package: Optional[PackageRequestDTO] = None

    
class AddOrderRequestDTO(BaseModel):
    external_ref: str
    tenant_id: Optional[str] = None
    customer_details: CustomerDetailsRequestDTO
    product_skus: List[ProductSkusRequestDTO]

class ConfirmShipmentRequestDTO(BaseModel):
    tenant_id: str
    order_id: str
    shipment_id: str
    order_status: enums.OrderStatus

class ShippingWebhookRequestDTO(BaseModel):
    provider: str
    tracking_reference: str
    tenant_id: str
    status: str
    occured_at: datetime
    raw_payload: dict
