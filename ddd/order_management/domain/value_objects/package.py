from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple
from ddd.order_management.domain import enums, exceptions

@dataclass(frozen=True)
class Package:
    weight: Decimal #in kg
    #weight_unit: str = "kg"
    dimensions: Tuple[int, int, int] # (length, width, height) in cm
    #dimensions_unit: str = "cm"

    def __post_init__(self):
        if self.weight <= Decimal("0"):
            raise exceptions.PackageException("Weight must be greater than zero.")
        if not isinstance(self.dimensions, tuple) and len(self.dimensions) == 3:
            raise TypeError("Dimensions must be a tuple of length 3 (length, width, height)")
        if any(d <= 0 for d in self.dimensions):
            raise exceptions.PackageException("All dimensions must be greater than zero.")