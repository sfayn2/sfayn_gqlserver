from __future__ import annotations
from dataclasses import dataclass

#right now only for Gues customer
@dataclass(frozen=True)    
class CustomerDetails:
    first_name: str
    last_name: str
    email: str

    def __post_init__(self):
        if not self.first_name or not self.last_name or not self.email:
            raise ValueError("Customer details are incomplete.")
        #TODO: validate email