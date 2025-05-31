import ast
from ddd.order_management.domain import value_objects, models
from vendor_management import models as django_vendor_models

class CouponMapper:

    @staticmethod
    def to_domain(coupon_code) -> value_objects.Coupon:
        #only care on coupon code & load the rest of attrs value from db
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon_code)
        if django_coupon.exists():
            return value_objects.Coupon(
                coupon_code=django_coupon.values_list("coupon_code", flat=True)[0],
                start_date=django_coupon.values_list("start_date", flat=True)[0],
                end_date=django_coupon.values_list("end_date", flat=True)[0],
                is_active=django_coupon.values_list("is_active", flat=True)[0],
            )