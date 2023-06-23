from ....delivery_domain import abstract_domain_models
from .delivery_package import DeliveryPackage
from .package_pricing import PackagePricing

class Delivery(abstract_domain_models.AggregateRoot):

    def __init__(self,
                 delivery_package: DeliveryPackage,
                 pickup_detail: str
                ):

        self._delivery_package = set()
        self._package_pricing = set()

    def add_package_pricing(self, package_pricing: PackagePricing):
        self._package_pricing.add(package_pricing)

    def get_package_pricings(self):
        return self._package_pricing

