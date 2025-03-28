import pytz
from datetime import datetime
from typing import List
from ddd.order_management.domain import repositories, enums, value_objects, exceptions
from vendor_management import models as django_vendor_models
from ddd.order_management.infrastructure import order_dtos

class DjangoVendorRepository(repositories.VendorRepository):

    def get_offers(self, vendor_name: str):
        offers = django_vendor_models.Offer.objects.filter(vendor__name=vendor_name, is_active=True).prefetch_related("coupon").values()
        offer_list = [
            { **offer, "coupons": list(django_vendor_models.Coupon.objects.filter(offer__id=offer.get("id")).values()) }
            for offer in offers
        ]

        final_offers = []
        for offer in offer_list:
            offer_dto = order_dtos.OfferStrategyDTO(**offer)
            try:
                final_offers.append(offer_dto.to_domain())
            except (exceptions.InvalidOfferOperation, ValueError) as e:
                #TODO send notification for invalid offer?
                print(f"DjangoVendorRepository.get_offer exception > {str(e)}")
                continue
        return final_offers


    def get_shipping_options(self, vendor_name: str):
        shipping_options = django_vendor_models.ShippingOption.filter(vendor__name=vendor_name)
        final_opts = []
        for option in shipping_options:
            ship_opt_dto = order_dtos.ShippingOptionStrategyDTO(**option)
            try:
                final_opts.append(ship_opt_dto.to_domain())
            except (ValueError) as e:
                print(f"DjangoVendorRepository.get_shipping_options exception > {str(e)}")
                continue
        return final_opts
