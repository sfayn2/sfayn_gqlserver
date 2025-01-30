from datetime import datetime
from ddd.order_management.domain import repositories
from vendor_management import models as django_vendor_models
from ddd.order_management.infrastructure import order_dtos

class DjangoVendorRepository(repositories.VendorRepository):

    def get_offers(self, vendor_name: str):
        offers = django_vendor_models.Offer.objects.filter(vendor__name=vendor_name, is_active=True).prefetch_related("coupon").values()
        offer_list = [
            { **offer, "coupons": list(django_vendor_models.Coupon.objects.filter(offer__id=offer.get("id")).values()) }
            for offer in offers
        ]
        offers_dto = order_dtos.VendorDTO.from_django_filters(offer_list)
        return offers_dto.model_dump().get("offers")

    def get_shipping_options(self, vendor_name: str):
        shipping_options = django_vendor_models.ShippingOption.filter(vendor__name=vendor_name)
        return list(shipping_options)
