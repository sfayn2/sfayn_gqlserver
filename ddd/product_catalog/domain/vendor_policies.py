from abc import ABC, abstractmethod
from ddd.product_catalog.domain import enums, exceptions, models

class VendorPolicy(ABC):
    @abstractmethod
    def get_allowed_transition(self, new_status: str):
        raise NotImplementedError

    @abstractmethod
    def can_approve(self, role):
        raise NotImplementedError

    @abstractmethod
    def validate_image(self, images):
        raise NotImplementedError

    @abstractmethod
    def validate_category(self, product):
        raise NotImplementedError
