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

    @abstractmethod
    def validate_image(self, images):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def validate_category(self, product):
        raise NotImplementedError("Subclasses must implement this method")

class StandardVendorPolicy(VendorPolicy):

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PUBLISHED.name],
    }

    def get_allowed_transition(self, new_status: enums.ProductStatus):
        return self.VALID_STATUS_TRANSITIONS.get(new_status.name)

    def can_approve(self, role):
        return True

    def validate_category(self, product: models.Product):
        if len(product.categories) < 1:
            raise ValueError("Standard vendors require at least one category")
        for category in product.categories:
            if category.parent is not None:
                raise ValueError("Standard vendors do not support nested categories")

    def validate_image(self, images):
        if len(images) > 1:
            raise ValueError("Standard vendors can only have one image")

class StandardVendorPolicyV2(StandardVendorPolicy):

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PUBLISHED.name],
    }

    def get_allowed_transition(self, new_status: enums.ProductStatus):
        return self.VALID_STATUS_TRANSITIONS.get(new_status.name)

    def can_approve(self, role):
        return True

    def validate_category(self, product):
        if product.categories[0].parent is None:
            raise ValueError("Custom vendors require a nested categories")

    def validate_image(self, images):
        if len(images) < 3:
            raise ValueError("Custom vendors must have at least 3 images")

class StandardVendorPolicyV3(StandardVendorPolicy):
    def validate_category(self, product):
        if product.categories[0].parent is None:
            raise ValueError("Standard Vendor policy version 3 requires a nested categories")

