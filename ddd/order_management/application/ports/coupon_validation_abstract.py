from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Validate coupon contract
# ==========
class CouponValidationAbstract(ABC):

    @abstractmethod
    def ensure_coupon_still_valid(self, coupon_code: str) -> None:
        raise NotImplementedError("Subclasses must implement this method")