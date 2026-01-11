from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from ddd.order_management.domain import enums


# ===========
# These DTOS response is the Main control of fields to expose to other layers
# =========

class ResponseDTO(BaseModel):
    success: bool
    message: str

# ====================
# Pydantic Response DTOs
# ====================

class MoneyResponseDTO(BaseModel):
    # required=True in Graphene maps to a non-Optional field in Pydantic
    amount: Decimal
    currency: str

class AddressResponseDTO(BaseModel):
    line1: str
    city: str
    country: str
    # required=False in Graphene maps to Optional[] in Pydantic
    line2: Optional[str] = None
    state: Optional[str] = None
    postal: Optional[str] = None

class PackageResponseDTO(BaseModel):
    # Not required by default in Graphene ObjectType
    weight_kg: Optional[Decimal] = None

class CustomerDetailsResponseDTO(BaseModel):
    customer_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None

class LineItemResponseDTO(BaseModel):
    product_sku: Optional[str] = None
    product_name: Optional[str] = None
    order_quantity: Optional[int] = None
    vendor_id: Optional[str] = None
    product_price: Optional[MoneyResponseDTO] = None
    package: Optional[PackageResponseDTO] = None

class ShipmentItemResponseDTO(BaseModel):
    # line_item is a nested object/field
    line_item: Optional[LineItemResponseDTO] = None
    quantity: Optional[int] = None
    shipment_item_id: Optional[str] = None

class ShipmentResponseDTO(BaseModel):
    shipment_id: Optional[str] = None
    shipment_address: Optional[AddressResponseDTO] = None
    shipment_provider: Optional[str] = None
    # Use the actual enum class from your domain models
    shipment_mode: Optional[enums.ShipmentMethod] = None

    # package details
    package_weight_kg: Optional[Decimal] = None
    package_length_cm: Optional[Decimal] = None
    package_width_cm: Optional[Decimal] = None
    package_height_cm: Optional[Decimal] = None

    # pickup mode details
    pickup_address: Optional[AddressResponseDTO] = None
    pickup_window_start: Optional[datetime] = None # Maps to graphene.DateTime
    pickup_window_end: Optional[datetime] = None
    pickup_instructions: Optional[str] = None

    tracking_reference: Optional[str] = None
    label_url: Optional[str] = None
    shipment_amount: Optional[MoneyResponseDTO] = None
    # Use the actual enum class from your domain models
    shipment_status: Optional[enums.ShipmentStatus] = None 
    shipment_items: Optional[List[ShipmentItemResponseDTO]] = None


class OrderResponseDTO(BaseModel):
    order_id: Optional[str] = None
    # Use List for graphene.List fields
    line_items: Optional[List[LineItemResponseDTO]] = None
    shipments: Optional[List[ShipmentResponseDTO]] = None
    customer_details: Optional[CustomerDetailsResponseDTO] = None
    currency: Optional[str] = None
    tenant_id: Optional[str] = None
    # Use the actual enum class from your domain models
    order_status: Optional[enums.OrderStatus] = None 
    payment_status: Optional[enums.PaymentStatus] = None 
    date_modified: Optional[datetime] = None 
    date_created: Optional[datetime] = None 

    class Config:
        use_enum_values = True

# use for shipping provider
class CreateShipmentResponseDTO(BaseModel):
    tracking_reference: str
    total_amount: MoneyResponseDTO
    label_url: str

class ProductSkusResponseDTO(BaseModel):
    product_sku: str
    order_quantity: int
    vendor_id: str
    product_name: str
    product_price: MoneyResponseDTO
    package: PackageResponseDTO

class AddOrderResponseDTO(BaseModel):
    external_ref: str
    tenant_id: str
    customer_details: CustomerDetailsResponseDTO
    product_skus: List[ProductSkusResponseDTO]

class ConfirmShipmentResponseDTO(BaseModel):
    tenant_id: str
    order_id: str
    shipment_id: str
    order_status: enums.OrderStatus

class ShippingWebhookResponseDTO(BaseModel):
    provider: str
    tracking_reference: str
    tenant_id: str
    status: str
    occured_at: datetime
    raw_payload: dict

class TenantResponseDTO(BaseModel):
    tenant_id: str
    configs: Dict[str, Any]