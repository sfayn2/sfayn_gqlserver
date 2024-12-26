from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.product_catalog.domain import enums, exceptions, models

class VendorPolicy(ABC):
    @abstractmethod
    def get_allowed_transition(self, new_status: enums.ProductStatus):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def can_approve(self, role):
        raise NotImplementedError("Subclasses must implement this method")

class DefaultVendorPolicy(VendorPolicy):

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PUBLISHED.name],
    }

    def get_allowed_transition(self, new_status: enums.ProductStatus):
        return self.VALID_STATUS_TRANSITIONS.get(new_status.name)

    def can_approve(self, role):
        return True


