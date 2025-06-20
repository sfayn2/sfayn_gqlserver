from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from order_management import models as django_snapshots

class DjangoCouponValidationService(ports.CouponValidationServiceAbstract):

    def ensure_coupon_is_valid(
        self, coupon_code: str, vendor_id: str
    ) -> value_objects.Coupon:

        vendor_coupon_snapshot = django_snapshots.VendorCouponSnapshot.objects.filter(
            coupon_code=coupon_code, vendor_id=vendor_id
        )

        if vendor_coupon_snapshot.exists():
            return django_mappers.CouponMapper.to_domain(vendor_coupon_snapshot)
        
        raise exceptions.CouponException(
            f"Coupon {coupon_code} is not offered by vendor {vendor_id}"
        )


