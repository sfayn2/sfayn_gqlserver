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

class StandardVendorPolicy(VendorPolicy):

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PUBLISHED.name],
    }

    def get_allowed_transition(self, new_status: str):
        return self.VALID_STATUS_TRANSITIONS.get(new_status)

    def can_approve(self, role):
        return True

    def validate_category(self, product):
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

    def get_allowed_transition(self, new_status: str):
        return self.VALID_STATUS_TRANSITIONS.get(new_status)

    def can_approve(self, role):
        return True

    def validate_category(self, product):
        if product.categories[0].parent is None:
            raise ValueError("Custom vendors require a nested categories")

    def validate_image(self, images):
        if len(images) < 3:
            raise ValueError("Custom vendors must have at least 3 images")

#django permission to have standard_policy & custom_policy?
POLICIES = {
    "standard": StandardVendorPolicy(),
    "standardV2": StandardVendorPolicyV2()
}

def get_policy(vendor_type):
    return POLICIES.get(vendor_type, StandardVendorPolicy())