from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects

class VendorAbstract(ABC):

    @abstractmethod
    def get_line_items(self, vendor_id: str, product_skus_input: List[ProductSkuDTO]) -> List[models.LineItem]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_offers(self) -> List[value_objects.OfferStrategy]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(self) -> List[value_objects.ShippingOptionStrategy]:
        raise NotImplementedError("Subclasses must implement this method")