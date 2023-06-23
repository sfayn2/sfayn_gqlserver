from ....delivery_domain import abstract_domain_models
from .delivery_package import DeliveryPackage

class Delivery(abstract_domain_models.AggregateRoot):

    def __init__(self,
                 delivery_package: DeliveryPackage,
                 pickup_detail: str
                ):

        self._delivery_package = set()
