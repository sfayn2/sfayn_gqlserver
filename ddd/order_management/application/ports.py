from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeVar
from ddd.order_management.domain import enums, value_objects, models, repositories
T = TypeVar("T")

# ========
# Payment contract
# ==========
class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayFactoryAbstract(ABC):

    @abstractmethod
    def get_payment_gateway(self, payment_method: enums.PaymentMethod) -> PaymentGatewayAbstract:
        raise NotImplementedError("Subclasses must implement this method")

# =====
# Shipping Option contract
# ========
class ShippingOptionStrategyAbstract(ABC):

    def __init__(self, strategy: value_objects.ShippingOptionStrategy):
        self.strategy = strategy

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if shipping option is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        raise NotImplementedError("Subclasses must implement this method")

class ShippingOptionStrategyServiceAbstract:

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def get_shipping_options(self, order: models.Order) -> List[value_objects.ShippingDetails]:
        raise NotImplementedError("Subclasses must implement this method")

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

class OfferStrategyServiceAbstract:        

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def apply_offers(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")


# ========
# Tax strategy contract
# =======

class TaxStrategyAbstract(ABC):
    @abstractmethod
    def apply(self, order: models.Order) -> value_objects.TaxResult:
        raise NotImplementedError("Subclasses must implement this method")

# ===
# UOW
# ===
class UnitOfWorkAbstract(ABC):

    def __enter__(self) -> T:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def rollback(self):
        raise NotImplementedError("Subclasses must implement this method")