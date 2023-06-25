from typing import List
from enum import IntEnum
from ....delivery_domain import abstract_domain_models
from .delivery_package import DeliveryPackage


class DeliveryStatus(IntEnum):
    PENDING_ACCEPTANCE = 4
    PICKUP_IN_PROGRESS = 5
    PICKED = 6
    ITEM_PICKED_UP = 7
    DELIVERED = 8
    UNDELIVERED = 9


class Delivery(abstract_domain_models.AggregateRoot):

    def __init__(self,
                 order_id: str,
                 delivery_packages: List[DeliveryPackage],
                ):

        self._delivery_package = set()
        for delivery_package in delivery_packages:
            self._delivery_package.add(delivery_package)

        #self._pickup_detail = pickup_detail > should be able to get from warehouse info? > line_item
        self._delivery_status = DeliveryStatus.PENDING_ACCEPTANCE

    def set_as_pick_up_in_progress(self):
        self._delivery_status = DeliveryStatus.PICKUP_IN_PROGRESS

    def set_as_picked_up(self):
        self._delivery_status = DeliveryStatus.ITEM_PICKED_UP
            




