from __future__ import annotations
import re
from dataclasses import dataclass
from ddd.order_management.domain import exceptions

@dataclass(frozen=True)    
class CustomerDetails:
    customer_id: str
    first_name: str
    last_name: str
    email: str

    def __post_init__(self):
        if not self.first_name or not self.last_name or not self.email:
            raise exceptions.CustomerDetailsException("Customer details fields (first_name, last_name, email) cannot be empty.")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise exceptions.CustomerDetailsException("Customer email is not valid.")