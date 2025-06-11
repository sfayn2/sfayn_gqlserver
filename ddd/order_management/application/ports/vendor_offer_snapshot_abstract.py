from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class VendorOfferSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_offers(self) -> List[dtos.VendorOfferSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_coupons_for_offers(self, offer_id: uuid.UUID) -> List[dtos.VendorCouponSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")