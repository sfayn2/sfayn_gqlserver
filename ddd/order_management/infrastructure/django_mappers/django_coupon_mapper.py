import ast
from ddd.order_management.domain import value_objects, models

class CouponMapper:

    @staticmethod
    def to_domain(django_coupon) -> value_objects.Coupon:
        return value_objects.Coupon(
            coupon_code=django_coupon.values_list("coupon_code", flat=True)[0],
            start_date=django_coupon.values_list("start_date", flat=True)[0],
            end_date=django_coupon.values_list("end_date", flat=True)[0],
            #is_active=django_coupon.values_list("is_active", flat=True)[0],
        )