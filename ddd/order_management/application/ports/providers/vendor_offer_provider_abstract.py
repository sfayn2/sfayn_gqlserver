from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class VendorOfferProviderAbstract(ABC):

    @abstractmethod
    def get_all_offers(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_coupons_for_offers(self):
        raise NotImplementedError("Subclasses must implement this method")