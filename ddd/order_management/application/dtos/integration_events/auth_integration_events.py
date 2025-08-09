import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List

#class ShippingAddressModel(BaseModel):
#    street: str
#    city: str
#    state: str
#    postal: int
#    country: str
#
#
#class ClaimsModel(BaseModel):
#
#    roles: List[str] = Field(default_factory=list)
#    email: str
#    given_name: Optional[str]
#    family_name: Optional[str]
#
#    # Optional: vendor specific fields
#    vendor_name: Optional[str]
#    vendor_country: Optional[str]
#    
#    # Optional: Shipping address fields?
#    shipping_address: Optional[ShippingAddressModel]

class UserLoggedInIntegrationEvent(BaseModel):
    event_type: str
    sub: str
    token_type: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)
    #claims: ClaimsModel

