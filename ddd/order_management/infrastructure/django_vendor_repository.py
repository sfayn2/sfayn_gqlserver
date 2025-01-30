from datetime import datetime
from ddd.order_management.domain import repositories
from vendor_management import models as django_vendor_models
from ddd.order_management.infrastructure import order_dtos

class DjangoVendorRepository(repositories.VendorRepository):

    def get_offers(self, vendor_name: str):
        offers = django_vendor_models.Offer.objects.filter(vendor__name=vendor_name, is_active=True).values()
        offers_dto = order_dtos.VendorDTO.from_django_filters(offers)
        return offers_dto.model_dump().get("offers")

    def get_shipping_options(self, vendor_name: str):
        shipping_options = django_vendor_models.ShippingOption.filter(vendor__name=vendor_name)
        return list(shipping_options)
