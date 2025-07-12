import uuid
from pydantic import BaseModel, root_validator
from typing import Dict, Optional, List

class UserLoggedInIntegrationEvent(BaseModel):
    event_type: str
    token_type: str
    sub: str
    tenant_id: str

    email: str
    given_name: Optional[str]
    family_name: Optional[str]
    roles: List[str] = Field(default_factory=list)

    # Optional: vendor specific fields
    vendor_name: Optional[str]
    vendor_country: Optional[str]
    
    # Optional: Shipping address fields?
    shipping_address: Optional[ShippingAddressModel]

