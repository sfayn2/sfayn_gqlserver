from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class CouponMapper:
    @staticmethod
    def to_domain(coupon_dto: dtos.CouponDTO) -> value_objects.Coupon:
        return value_objects.Coupon(**coupon_dto.model_dump())