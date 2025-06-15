import pytz, uuid
from datetime import datetime
from typing import List
from ddd.order_management.domain import repositories, enums, value_objects, exceptions
from order_management import models as django_snapshots
from ddd.order_management.infrastructure import django_mappers

class DjangoVendorRepositoryImpl(repositories.VendorAbstract):

    def get_offers(self, vendor_id: uuid.UUID) -> List[value_objects.OfferStrategy]:
        offers = django_snapshots.VendorOfferSnapshot.objects.filter(vendor_id=vendor_id, is_active=True).prefetch_related("coupon").values()
        offer_list = [
            { **offer, "coupons": list(django_snapshots.VendorCouponSnapshot.objects.filter(offer_id=offer.get("offer_id")).values()) }
            for offer in offers
        ]

        final_offers = []
        for offer in offer_list:
            try:
                final_offers.append(django_mappers.OfferStrategyMapper.to_domain(offer))
            except exceptions.OfferStrategyException as e:
                #TODO send notification for invalid offer?
                print(f"DjangoVendorRepository.get_offer exception > {str(e)}")
                continue
        return final_offers


    def get_shipping_options(self, vendor_id: uuid.UUID) -> List[value_objects.ShippingOptionStrategy]:
        shipping_options = django_snapshots.VendorShippingOptionSnapshot.objects.filter(vendor_id=vendor_id, is_active=True)
        final_opts = []
        for option in shipping_options.values():
            option.pop("id")
            try:
                final_opts.append(django_mappers.ShippingOptionStrategyMapper.to_domain(option))
            except (ValueError) as e:
                print(f"DjangoVendorRepository.get_shipping_options exception > {str(e)}")
                continue
        return final_opts
