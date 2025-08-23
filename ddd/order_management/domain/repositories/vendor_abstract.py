from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects

class VendorAbstract(ABC):

    @abstractmethod
    def get_line_items(
        self, 
        tenant_id: str,
        vendor_id: str, 
        product_skus_input: List[ProductSkuDTO]
    ) -> List[models.LineItem]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_offers(
        self, 
        tenant_id: str,
        vendor_id: str
    ) -> List[value_objects.OfferStrategy]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(
        self,
        tenant_id: str,
        vendor_id: str
    ) -> List[dtos.VendorShippingOptionSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")