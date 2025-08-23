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
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if offer is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def apply(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")
