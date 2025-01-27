from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.infrastructure import dtos

class CheckoutResponseDTO(BaseModel):
    order_id: str
    order_status: str
    message: str
