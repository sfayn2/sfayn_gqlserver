import ast
from ddd.order_management.domain import value_objects, models
from vendor_management import models as django_vendor_models

class CouponMapper:

    @staticmethod
    def to_domain(coupon_code) -> value_objects.Coupon:
        #only care on coupon code & load the rest of attrs value from db
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon_code)
        if django_coupon.exists():
            django_coupon2 = django_coupon.values().first()
            django_coupon2.pop("id")
            return value_objects.Coupon(**django_coupon2)