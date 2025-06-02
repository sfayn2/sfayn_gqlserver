from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Product Catalog contract
# ==========
class StockValidationServiceAbstract(ABC):

    @abstractmethod
    def ensure_items_in_stock(self, items: List[models.LineItem]) -> None:
        raise NotImplementedError("Subclasses must implement this method")

