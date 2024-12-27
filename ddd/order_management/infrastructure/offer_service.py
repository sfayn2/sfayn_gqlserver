from ddd.order_management.domain.services import offer_policies
from django.contrib.auth.models import Group
from django.conf import settings

class OfferPolicyService:
    POLICIES = {
        "default_offer_policy": offer_policies.DefaultOfferPolicy
    }

    def get_policy(self, vendor_id: int):

        #START <multi vendor policy>
        vendor_grp = Group.objects.filter(id=vendor_id)
        for perm, policy_impl in self.POLICIES.items():
            if vendor_grp.filter(permissions__codename=perm).exists():
                return policy_impl()

        #default   
        return offer_policies.DefaultOfferPolicy()
        #END <multi vendor policy>
