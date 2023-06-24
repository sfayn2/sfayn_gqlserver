from typing import List
from ....delivery_domain import abstract_domain_models
from ._delivery_package import DeliveryPackage
from ._pickup_detail import PickupDetail
from ._delivery_status import DeliveryStatus

class Delivery(abstract_domain_models.AggregateRoot):

    def __init__(self,
                 delivery_packages: List[DeliveryPackage],
                 pickup_detail: PickupDetail
                ):

        self._delivery_package = set()
        for delivery_package in delivery_packages:
            self._delivery_package.add(delivery_package)

        self._pickup_detail = pickup_detail
        self._delivery_status = DeliveryStatus.PENDING_ACCEPTANCE

    def set_as_pick_up_in_progress(self):
        self._delivery_status = DeliveryStatus.PICKUP_IN_PROGRESS

    def set_as_picked_up(self):
        self._delivery_status = DeliveryStatus.ITEM_PICKED_UP
            




