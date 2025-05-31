from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import models, value_objects, repositories

# ==========================
# Offer Strategy Contract
# =================
class OfferStrategyAbstract(ABC):
    def __init__(self, strategy: value_objects.OfferStrategy, order: models.Order):
        self.strategy = strategy
        self.order = order

    @abstractmethod
    def apply(self):
        raise NotImplementedError("Subclasses must implement this method")

    def validate_coupon(self):
        #reuse if the offer is based on coupon
        for coupon in self.order.coupons:
            if self.strategy.required_coupon == True and coupon in [item for item in self.strategy.coupons]:
                return True
        return False

    def validate_minimum_quantity(self):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_quantity") and (sum(item.order_quantity for item in self.order.line_items) >= self.strategy.conditions.get("minimum_quantity"))

    def validate_minimum_order_total(self):
        return self.strategy.conditions and self.strategy.conditions.get("minimum_order_total") and (self.order.total_amount.amount >= self.strategy.conditions.get("minimum_order_total"))

# ================
# Offer Strategy Service
# ==================

class OfferStrategyServiceAbstract(ABC):        

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def evaluate_applicable_offers(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")
