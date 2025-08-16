from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects

class CustomerAbstract(ABC):

    @abstractmethod
    def get_customer_details(self, tenant_id: str, customer_id: str) -> value_objects.CustomerDetails:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_addresses(self, tenant_id: str, customer_id: str) -> List[value_objects.CustomerDetails]:
        raise NotImplementedError("Subclasses must implement this method")