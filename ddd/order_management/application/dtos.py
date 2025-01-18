from pydantic import BaseModel
import uuid
from typing import Optional, List
from ddd.order_management.domain import value_objects, models

class CheckoutRequestDTO(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    address: value_objects.Address
    line_items: List[models.LineItem]


class CheckoutResponseDTO(BaseModel):
    order_id: str
    status: str
    message: str
