from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from ddd.order_management.domain import exceptions

@dataclass(frozen=True)
class Address:
    line1: str
    city: str
    country: str
    line2: Optional[str] = None
    state: Optional[str] = None
    postal: Optional[int] = None

