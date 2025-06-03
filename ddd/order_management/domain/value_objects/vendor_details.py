from __future__ import annotations
import uuid
from dataclasses import dataclass

@dataclass(frozen=True) 
class VendorDetails:
    id: uuid.UUID
    name: str
    country: str