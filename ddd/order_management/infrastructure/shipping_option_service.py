from ddd.order_management.domain import shipping_option_policies
from django.contrib.auth.models import Group
from django.conf import settings

class ShippingPolicyService:
    POLICIES = {
        "default_shipping_option_policy": shipping_option_policies.DefaultShippingOptionPolicy
    }

    def get_policy(self, vendor_id: int):

        #START <multi vendor policy>
        vendor_grp = Group.objects.filter(id=vendor_id)
        for perm, policy_impl in self.POLICIES.items():
            if vendor_grp.filter(permissions__codename=perm).exists():
                return policy_impl()

        #default   
        return shipping_option_policies.DefaultShippingOptionPolicy()
        #END <multi vendor policy>
