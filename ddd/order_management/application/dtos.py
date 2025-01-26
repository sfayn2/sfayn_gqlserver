from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import value_objects, models
from ddd.order_management.infrastructure import dtos

class CheckoutRequestDTO(BaseModel):
    customer_details: dtos.CustomerDetailsDTO
    address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]

class CheckoutResponseDTO(BaseModel):
    order_id: str
    order_status: str
    message: str
