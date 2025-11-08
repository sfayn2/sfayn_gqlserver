from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
from ddd.order_management.domain import exceptions

@dataclass(frozen=True)
class CustomerDetails:
    customer_name: str
    customer_email: str
    customer_id: Optional[str] = None