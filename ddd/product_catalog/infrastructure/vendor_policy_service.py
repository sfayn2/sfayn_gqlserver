from ddd.product_catalog.domain import vendor_policies
from django.contrib.auth.models import Group
from django.conf import settings

class VendorPolicyService:
    # permission cn do multi vendor policy?  # should this be in domain layer??
    POLICIES = {
        "vendor_standard_policy": vendor_policies.StandardVendorPolicy,
        "vendor_standard_v2_policy": vendor_policies.StandardVendorPolicyV2,
    }

    def get_policy(self, vendor_id: int):

        #START <multi vendor policy>
        vendor_grp = Group.objects.filter(id=vendor_id)
        for perm, policy_impl in self.POLICIES.items():
            if vendor_grp.filter(permissions__codename=perm).exists():
                return policy_impl()

        #default   
        return vendor_policies.StandardVendorPolicy()
        #END <multi vendor policy>
