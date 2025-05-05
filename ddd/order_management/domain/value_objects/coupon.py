from __future__ import annotations
import pytz
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Coupon:
    coupon_code: str
    start_date: datetime
    end_date: datetime
    is_active: bool

    def __post_init__(self):
        if not self.coupon_code:
            raise ValueError("Coupon code cannot be empty.")

        if not (self.is_active and datetime.now(pytz.utc) >= self.start_date and datetime.now(pytz.utc) <= self.end_date):
            raise ValueError(f"Coupon code {self.coupon_code} no longer valid.")


