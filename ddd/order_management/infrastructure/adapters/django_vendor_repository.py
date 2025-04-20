import pytz
from datetime import datetime
from typing import List
from ddd.order_management.domain import repositories, enums, value_objects, exceptions
from vendor_management import models as django_vendor_models
from ddd.order_management.infrastructure import infra_mappers

class DjangoVendorRepositoryImpl(repositories.VendorAbstract):

    def get_offers(self, vendor_name: str):
        offers = django_vendor_models.Offer.objects.filter(vendor__name=vendor_name, is_active=True).prefetch_related("coupon").values()
        offer_list = [
            { **offer, "coupons": list(django_vendor_models.Coupon.objects.filter(offer__id=offer.get("id")).values()) }
            for offer in offers
        ]

        final_offers = []
        for offer in offer_list:
            offer_dto =  infra_mappers.OfferStrategyMapper.to_dto(offer)
            try:
                final_offers.append(infra_mappers.OfferStrategyMapper.to_domain(offer_dto))
            except (exceptions.InvalidOfferOperation, ValueError) as e:
                #TODO send notification for invalid offer?
                print(f"DjangoVendorRepository.get_offer exception > {str(e)}")
                continue
        return final_offers

    #def get_vendor_details(self, vendor_name: str):
    #    vendor_details = django_vendor_models.Vendor.objects.filter(vendor__name=vendor_name, is_active=True)
    #    if not vendor_details.exists():
    #        raise exceptions.InvalidVendorDetails(f"Vendor details {vendor_name} not found.")

    #    return order_dtos.VendorDetailsDTO.from_django_filter(vendor_details.values()).to_domain()

    def get_shipping_options(self, vendor_name: str):
        shipping_options = django_vendor_models.ShippingOption.objects.filter(vendor__name=vendor_name, is_active=True)
        final_opts = []
        for option in shipping_options.values():
            option.pop("id")
            ship_opt_dto = infra_mappers.ShippingOptionStrategyMapper.to_dto(option)
            try:
                final_opts.append(infra_mappers.ShippingOptionStrategyMapper.to_domain(ship_opt_dto))
            except (ValueError) as e:
                print(f"DjangoVendorRepository.get_shipping_options exception > {str(e)}")
                continue
        return final_opts
