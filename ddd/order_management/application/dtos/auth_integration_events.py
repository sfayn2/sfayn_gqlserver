import uuid
from pydantic import BaseModel, root_validator
from typing import Dict, Optional, List

class RealmAccessModel(BaseModel):
    roles: List[str] = Field(default_factory=list)

class ShippingAddressModel(BaseModel):
    street: str
    city: str
    postal: int
    state: str
    country: str


class ClaimsModel(BaseModel):
    tenant_id: str
    email: str
    given_name: Optional[str]
    family_name: Optional[str]
    realm_access: RealmAccessModel

    # Optional: vendor specific fields
    vendor_name: Optional[str]
    vendor_country: Optional[str]
    
    # Optional: Shipping address fields?
    shipping_address: Optional[ShippingAddressModel]

class UserLoggedInIntegrationEvent(BaseModel):
    event_type: str
    user_id: str
    claims: ClaimsModel
