from __future__ import annotations
import uuid
from dataclasses import dataclass
from ddd.order_management.domain import enums, exceptions

#TODO post-init validation is missing
@dataclass(frozen=True) 
class VendorDetails:
    vendor_id: str
    name: str
    country: str

