from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Product Catalog contract
# ==========
class StockValidationAbstract(ABC):

    @abstractmethod
    def ensure_items_in_stock(self, tenant_id: str, skus: List[dtos.ProductSkusDTO] ) -> None:
        raise NotImplementedError("Subclasses must implement this method")

