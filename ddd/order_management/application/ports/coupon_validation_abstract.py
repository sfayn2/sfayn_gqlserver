from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

# ========
# Validate coupon contract
# ==========
class CouponValidationServiceAbstract(ABC):

    @abstractmethod
    def ensure_coupon_is_valid(self, coupon_code: str, vendor_id: str) -> value_objects.Coupon:
        raise NotImplementedError("Subclasses must implement this method")