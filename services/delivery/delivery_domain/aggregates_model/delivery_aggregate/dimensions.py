from ....delivery_domain import abstract_domain_models
from dataclasses import dataclass
from decimal import Decimal

from enum import StrEnum

class Units(StrEnum):
    cm = "cm"

@dataclass(frozen=True)
class Dimensions(abstract_domain_models.ValueObject):
    height:  Decimal
    length:  Decimal
    width:  Decimal
    units:  Units

    def __post_init__(self):
        if self.height < 0:
            raise "Invalid height value!"

        if self.length < 0:
            raise "Invalid length value!"

        if self.length < 0:
            raise "Invalid width value!"

        if self.units not in list(map(str, Units)):
            raise "Invalid dimensions unit!"