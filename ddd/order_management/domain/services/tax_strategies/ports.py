from __future__ import annotations
from typing import List, Tuple
from abc import ABC, abstractmethod
from ddd.order_management.domain import models, value_objects

# ========
# Tax strategy contract
# =======

class TaxStrategyAbstract(ABC):

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if taxes is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def calculate_tax(self, order: models.Order) -> value_objects.TaxResult:
        raise NotImplementedError("Subclasses must implement this method")
