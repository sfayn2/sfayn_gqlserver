from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import enums
from ddd.order_management.infrastructure import order_dtos

class OrderResponseDTO(BaseModel):
    order_id: str
    order_status: str
    success: bool
    message: str
    shipping_details: order_dtos.ShippingDetailsDTO
    tax_details: List[str]
    offer_details: List[str]
    tax_amount: order_dtos.MoneyDTO
    total_discounts_fee: order_dtos.MoneyDTO
    final_amount: order_dtos.MoneyDTO


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