
from ....delivery_domain import abstract_domain_models
from dataclasses import dataclass

@dataclass(frozen=True)
class DeliveryAddress(abstract_domain_models.ValueObject):
    address:  str
    postal:  int
    country:  str
    region:  str

    def __post_init__(self):
        if self.address is None:
            raise "Invalid address value!"

        if self.postal is None:
            raise "Invalid postal value!"

        if self.country is None:
            raise "Invalid country value!"

        if self.region is None:
            raise "Invalid region value!"
