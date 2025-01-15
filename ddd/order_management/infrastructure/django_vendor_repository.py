from ddd.order_management.domain import repositories
from vendor_management import models as django_vendor_models

class DjangoVendorRepository(repositories.VendorRepository):

    def get_offers(self, vendor_name: str):
        offers = django_vendor_models.Offer.objects.filter(vendor__name=vendor_name)
        return list(offers)

    def get_shipping_options(self, vendor_name: str):
        shipping_options = django_vendor_models.ShippingOption.filter(vendor__name=vendor_name)
        return list(shipping_options)
