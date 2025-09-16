from __future__ import annotations
import pytz
from dataclasses import dataclass
from datetime import datetime
from ddd.order_management.domain import exceptions
from ddd.order_management.domain.services import DomainClock

@dataclass(frozen=True)
class Coupon:
    coupon_code: str
    start_date: datetime
    end_date: datetime
    #is_active: bool

    #def __post_init__(self):
    #    if not self.coupon_code:
    #        raise exceptions.CouponException("Coupon code cannot be empty.")

    #    #if not (DomainClock.now() >= self.start_date and DomainClock.now() <= self.end_date):
    #    #    raise exceptions.CouponException(f"Coupon code {self.coupon_code} no longer valid.")


