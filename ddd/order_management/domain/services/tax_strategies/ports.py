from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import models, value_objects

# ========
# Tax strategy contract
# =======

class TaxStrategyAbstract(ABC):
    @abstractmethod
    def apply(self, order: models.Order) -> value_objects.TaxResult:
        raise NotImplementedError("Subclasses must implement this method")