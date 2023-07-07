from dataclasses import dataclass
from ... import abstract_domain_models

from enum import IntEnum

class FulfillmentStatus(IntEnum):
    NOT_FULFILLED = 0
    FULFILLED = 1
    CANCELLED = 2

@dataclass(unsafe_hash=True)
class FulfillmentItem(abstract_domain_models.Entity):
    _item_sku: str #TODO valueobject?

    def __post_init__(self):
        self.set_as_not_fulfilled()

    def set_tracking_number(self, tracking_number: str):
        self._tracking_number = tracking_number

    def set_as_not_fulfilled(self):
        self._fulfillment_status = FulfillmentStatus.NOT_FULFILLED

    def set_fulfilled(self):
        self._fulfillment_status = FulfillmentStatus.FULFILLED

    def set_cancelled(self):
        self._fulfillment_status = FulfillmentStatus.CANCELLED
