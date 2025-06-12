from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class VendorShippingOptionSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_shipping_options(self) -> List[dtos.VendorShippingOptionSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")