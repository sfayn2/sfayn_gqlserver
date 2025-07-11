from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class CustomerSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_customers(self) -> List[dtos.CustomerDetailSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_customer_address(self, customer_id: str) -> List[dtos.CustomerAddressSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")

