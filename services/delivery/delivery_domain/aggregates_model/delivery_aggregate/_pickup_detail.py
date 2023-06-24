
from ....delivery_domain import abstract_domain_models
from .delivery_address import DeliveryAddress
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class PickupDetail(abstract_domain_models.ValueObject):
    _name: str
    _contact_number: int 
    _pickup_address: DeliveryAddress  #just reuse same value object
    _pickup_pincode: int
    _pickup_remark: str
