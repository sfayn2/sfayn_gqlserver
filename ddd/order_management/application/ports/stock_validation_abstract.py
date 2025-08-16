from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Product Catalog contract
# ==========
class StockValidationAbstract(ABC):

    @abstractmethod
    def ensure_items_in_stock(self, tenant_id: str, items: List[models.LineItem]) -> None:
        raise NotImplementedError("Subclasses must implement this method")

