from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import models, value_objects, repositories

# ==========================
# Offer Strategy Contract
# =================
class OfferStrategyAbstract(ABC):
    def __init__(self, strategy: value_objects.OfferStrategy):
        self.strategy = strategy

    @abstractmethod
    def apply(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_coupon(self, order: models.Order):
        #reuse if the offer is based on coupon
        for coupon in order.coupons:
            if self.strategy.required_coupon == True and coupon in [item for item in self.strategy.coupons]:
                return True
        return False

    def validate_minimum_quantity(self, order:models.Order):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_quantity") and (sum(item.order_quantity for item in order.line_items) >= self.strategy.conditions.get("minimum_quantity"))

    def validate_minimum_order_total(self, order:models.Order):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_order_total") and (order.total_amount.amount >= self.strategy.conditions.get("minimum_order_total"))

# ================
# Offer Strategy Service
# ==================

class OfferStrategyServiceAbstract(ABC):        

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def apply_offers(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")
