from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True) 
class VendorDetails:
    name: str
    country: str