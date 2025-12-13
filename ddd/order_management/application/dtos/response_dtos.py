from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from .dtos import CustomerDetailsDTO, MoneyDTO, ShipmentItemDTO, LineItemDTO
from ddd.order_management.domain import enums

class ResponseDTO(BaseModel):
    success: bool
    message: str

class ShipmentItemResponseDTO(BaseModel):
    product_sku: str
    vendor_id: str
    quantity: int

class OrderResponseDTO(BaseModel):
    order_id: str
    tenant_id: str
    currency: str
    customer_details: CustomerDetailsDTO
    order_status: enums.OrderStatus
    payment_status: enums.PaymentStatus
    line_items: List[LineItemDTO]
    shipments: List[ShipmentItemResponseDTO]
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None

    class Config:
        use_enum_values = True

# use for shipping provider
class CreateShipmentResponseDTO(BaseModel):
    tracking_reference: str
    total_amount: MoneyDTO
    label_url: str