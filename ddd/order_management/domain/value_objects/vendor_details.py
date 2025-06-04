from __future__ import annotations
import uuid
from dataclasses import dataclass

#TODO post-init validation is missing
@dataclass(frozen=True) 
class VendorDetails:
    id: uuid.UUID
    name: str
    country: str

