from __future__ import annotations
from typing import List
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions

class DjangoCouponValidationAdapter(ports.CouponValidationAbstract):

    def ensure_coupon_still_valid(self, coupon_code: str, vendor_name: str) -> None:
        return django_mappers.CouponMapper.to_domain(coupon_code=coupon_code, vendor_name=vendora_name)


