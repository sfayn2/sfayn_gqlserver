from ....delivery_domain import abstract_domain_models
from dataclasses import dataclass
from decimal import Decimal

from enum import StrEnum

class Units(StrEnum):
    kg = "kg"

@dataclass(frozen=True)
class Weight(abstract_domain_models.ValueObject):
    value:  Decimal
    units:  Units

    def __post_init__(self):
        if self.value < 0:
            raise "Invalid weight value!"

        if self.units not in list(map(str, Units)):
            raise "Invalid weight unit!"