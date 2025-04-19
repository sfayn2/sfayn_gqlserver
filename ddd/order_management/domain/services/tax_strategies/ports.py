from __future__ import annotations
from typing import List, Tuple
from abc import ABC, abstractmethod
from ddd.order_management.domain import models, value_objects

# ========
# Tax strategy contract
# =======

class TaxStrategyAbstract(ABC):
    @abstractmethod
    def calculate_tax(self, order: models.Order) -> value_objects.TaxResult:
        raise NotImplementedError("Subclasses must implement this method")

class TaxStrategyServiceAbstract(ABC):

    @abstractmethod
    def calculate_all_taxes(self, order: models.Order, tax_strategies: List[TaxStrategyAbstract]) -> Tuple[value_objects.Money, List[str]]:
        raise NotImplementedError("Subclasses must implement this method")
