from abc import ABC, abstractmethod
from ddd.product_catalog.domain import enums, exceptions, models

class VendorPolicy(ABC):
    @abstractmethod
    def get_allowed_transition(self, new_status: str):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def can_approve(self, role):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def validate_image(self, images):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def validate_category(self, product):
        raise NotImplementedError("Subclasses must implement this method")
