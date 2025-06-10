from __future__ import annotations
from order_management import models as django_snapshots


class DjangoVendorOfferSnapshotSync:
    def __init__(self, vendor_offer_provider: VendorOfferSnapshotAbstract):
        self.vendor_offer_provider = vendor_offer_provider

    def sync(self):
        django_snapshots.VendorOfferSnapshot.objects.all().delete()
        django_snapshots.VendorCouponSnapshot.objects.all().delete()

        offers = self.vendor_offer_provider.get_all_offers()
        for offer in offers:
            django_snapshots.VendorOfferSnapshot.create(**offers.model_dump())
            coupons = self.vendor_offer_provider.get_coupons_for_offer(offer.vendor_id)
            for coupon in coupons:
                django_snapshots.VendorCouponSnapshot.create(**coupon.model_dump())