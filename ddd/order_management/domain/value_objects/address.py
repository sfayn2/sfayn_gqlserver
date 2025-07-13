from __future__ import annotations
from dataclasses import dataclass
from ddd.order_management.domain import exceptions

@dataclass(frozen=True)
class Address:
    street: str
    city: str
    postal: int
    country: str
    state: str
    # make use of country to country code converter if require?

    def __post_init__(self):
        if not self.street or not self.city or not self.postal or not self.state or not self.country:
            raise exceptions.AddressException("Address fields (street, city, postal, country, state) cannot be empty.")
        if not isinstance(self.postal, int) or self.postal <= 0:
            raise exceptions.AddressException(f"Invalid postal code {self.postal}. It must be a positive integer.")
        #TODO: validate country & state?

    def is_international(self, origin_country: str) -> bool:
        return self.country != origin_country

