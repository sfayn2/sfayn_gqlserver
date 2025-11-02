from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple
from ddd.order_management.domain import enums, exceptions

@dataclass(frozen=True)
class Package:
    weight_kg: Decimal #in kg
    dimensions_cm: Tuple[Decimal, Decimal, Decimal] # (length, width, height) in cm

    def __post_init__(self):
        if self.weight_kg <= Decimal("0"):
            raise exceptions.PackageException("Weight must be greater than zero.")
        if not isinstance(self.dimensions_cm, tuple) and len(self.dimensions_cm) == 3:
            raise TypeError("Dimensions must be a tuple of length 3 (length, width, height)")
        if any(d <= 0 for d in self.dimensions_cm):
            raise exceptions.PackageException("All dimensions must be greater than zero.")
