from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class VendorProductSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_products(self) -> List[dtos.VendorProductSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")
