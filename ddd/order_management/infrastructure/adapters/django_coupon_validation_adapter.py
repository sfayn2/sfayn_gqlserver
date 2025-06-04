from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from vendor_management import models as django_vendor_models

class DjangoCouponValidationAdapter(ports.CouponValidationAbstract):

    def ensure_coupon_is_valid(self, coupon_code: str, vendor_id: uuid.UUID) -> Union[None, value_objects.Coupon]:
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=item, offer__vendor__vendor_id=vendor_id)
        if django_coupon.exists():
            return django_mappers.CouponMapper.to_domain(django_coupon)


