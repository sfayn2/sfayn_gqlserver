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
                 delivery_type: int,
                 delivery_price: int,
                 delivery_packages: List[DeliveryPackage],
                 delivery_remark: str
                ):
            
        if not order_id:
            raise "Missing order id!"

        if not delivery_type:
            raise "Missing delivery type!"

        self._delivery_package = set()
        for delivery_package in delivery_packages:
            self._delivery_package.add(delivery_package)

        self._delivery_status = DeliveryStatus.PENDING_ACCEPTANCE
        self._delivery_type = delivery_type

    def set_as_pick_up_in_progress(self):
        self._delivery_status = DeliveryStatus.PICKUP_IN_PROGRESS

    def set_as_picked_up(self):
        self._delivery_status = DeliveryStatus.ITEM_PICKED_UP

            




