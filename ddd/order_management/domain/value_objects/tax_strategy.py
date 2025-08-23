from __future__ import annotations
import pytz
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict, Union
from datetime import datetime
from ddd.order_management.domain import enums, exceptions
from .coupon import Coupon

@dataclass(frozen=True) 
class TaxStrategy:
    tax_type: enums.TaxType
    inclusive: bool
    rate: Decimal
    conditions: dict
    is_active: bool
