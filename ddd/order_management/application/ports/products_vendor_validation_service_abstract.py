from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Products Vendor contract
# ==========
class ProductsVendorValidationServiceAbstract(ABC):

    @abstractmethod
    def ensure_items_vendor_is_valid(self, items: List[models.LineItem]) -> None:
        raise NotImplementedError("Subclasses must implement this method")
