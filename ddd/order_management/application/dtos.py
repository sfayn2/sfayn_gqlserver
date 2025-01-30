from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.infrastructure import dtos

class CheckoutResponseDTO(BaseModel):
    order_id: str
    order_status: str
    success: bool
    message: str

class PlaceOrderResponseDTO(BaseModel):
    order_id: str
    order_status: str
    success: bool
    message: str
    tax_details: List[str]
    offer_details: List[str]
    tax_amount: dtos.MoneyDTO
    total_discounts_fee: dtos.MoneyDTO
    final_amount: dtos.MoneyDTO

class ResponseWExceptionDTO(BaseModel):
    success: bool
    message: str
