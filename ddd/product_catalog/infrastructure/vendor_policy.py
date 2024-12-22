from ddd.product_catalog.domain import vendor_policies, enums, models
from django.contrib.auth.models import Group
from django.conf import settings

class StandardVendorPolicy(vendor_policies.VendorPolicy):

    VALID_STATUS_TRANSITIONS = {
        enums.ProductStatus.DRAFT.name : [enums.ProductStatus.PUBLISHED.name],
    }

    def get_allowed_transition(self, new_status: str):
        return self.VALID_STATUS_TRANSITIONS.get(new_status)

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

class StandardVendorPolicyV3(StandardVendorPolicy):
    def validate_category(self, product):
        if product.categories[0].parent is None:
            raise ValueError("Standard Vendor policy version 3 requires a nested categories")

# permission cn do multi vendor policy?
POLICIES = {
    "vendor_standard_policy": StandardVendorPolicy,
    "vendor_standard_v2_policy": StandardVendorPolicyV2,
    "vendor_standard_v3_policy": StandardVendorPolicyV3
}

def get_policy(vendor_id: int):

    #START <multi vendor policy>
    vendor_grp = Group.objects.filter(id=vendor_id)
    for perm, policy_impl in POLICIES.items():
        if vendor_grp.filter(permissions__codename=perm).exists():
            return policy_impl()

    #default   
    return StandardVendorPolicy()
    #END <multi vendor policy>
