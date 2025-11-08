from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from .dtos import CustomerDetailsDTO, MoneyDTO

class ResponseDTO(BaseModel):
    success: bool
    message: str

class OrderResponseDTO(BaseModel):
    tenant_id: str
    customer_details: CustomerDetailsDTO

    class Config:
        use_enum_values = True

# use for shipping provider
class CreateShipmentResponseDTO(BaseModel):
    tracking_reference: str
    total_amount: MoneyDTO
    label_url: str