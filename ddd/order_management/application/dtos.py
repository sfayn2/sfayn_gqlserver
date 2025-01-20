from pydantic import BaseModel
import uuid
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import value_objects, models, dtos

class CheckoutRequestDTO(BaseModel):
    customer_details: dtos.CustomerDetailsDTO
    address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]

    def to_domain(self) -> models.Order:
        line_items = [item.to_domain() for item in self.line_items]
        return models.Order(
            customer_details=self.customer_details.to_domain(),
            destination=self.address.to_domain(),
            line_items=line_items
        )



class CheckoutResponseDTO(BaseModel):
    order_id: str
    order_status: str
    message: str
