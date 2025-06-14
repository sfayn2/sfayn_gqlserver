from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class VendorDetailsSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_vendors(self) -> List[dtos.VendorDetailsSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")
