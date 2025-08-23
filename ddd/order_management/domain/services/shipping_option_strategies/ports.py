from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ddd.order_management.domain import models, value_objects, repositories
# =====
# Shipping Option contract
# ========
class ShippingOptionStrategyAbstract(ABC):


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

class ShippingOptionStrategyServiceAbstract(ABC):

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def get_applicable_shipping_options(
                self, 
                order: models.Order, 
                vendor_shipping_options: List[value_objects.ShippingOptionStrategy]
            ) -> List[value_objects.ShippingDetails]:
        raise NotImplementedError("Subclasses must implement this method")
