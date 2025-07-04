from __future__ import annotations
from dataclasses import dataclass
from ddd.order_management.domain import exceptions

#right now only for Gues customer
@dataclass(frozen=True)    
class CustomerDetails:
    customer_id: str
    first_name: str
    last_name: str
    email: str

    def __post_init__(self):
        if not self.first_name or not self.last_name or not self.email:
            raise exceptions.CustomerDetailsException("Customer details are incomplete.")
        #TODO: validate email