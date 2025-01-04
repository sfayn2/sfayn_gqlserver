from ddd.order_management.domain import repositories

class DjangoVendorRepository(repositories.VendorRepository):

    def get_offers(self, vendor_name: str):
        return super().get_offers()

    def get_shipping_options(self):
        return super().get_shipping_options()
