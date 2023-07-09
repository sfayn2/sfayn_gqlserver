from dataclasses import dataclass
from ... import abstract_domain_models

from enum import IntEnum

class FulfillmentStatus(IntEnum):
    NOT_FULFILLED = 0
    PROCESSING = 1
    FULFILLED = 2
    CANCELLED = 3

@dataclass(unsafe_hash=True)
class FulfillmentItem(abstract_domain_models.Entity):
    _item_sku: str #TODO valueobject?
    _tracking_number: str
    _fulfillment_status: FulfillmentStatus  = FulfillmentStatus.NOT_FULFILLED

    #def __post_init__(self):
    #    self.set_as_not_fulfilled()

    def get_fulfillment_status(self):
        return self._fulfillment_status

    def set_tracking_number(self, tracking_number: str):
        self._tracking_number = tracking_number

    def set_as_fulfilled(self):
        if not self._fulfillment_status == FulfillmentStatus.PROCESSING:
            raise "Not allowed to set fulfillment as fulfilled!"
        self._fulfillment_status = FulfillmentStatus.FULFILLED

    def set_as_cancelled(self):
        self._fulfillment_status = FulfillmentStatus.CANCELLED

    def set_as_processing(self):
        if not self._fulfillment_status == FulfillmentStatus.NOT_FULFILLED:
            raise "Not allowed to set fulfillment as processing!"
        self._fulfillment_status = FulfillmentStatus.PROCESSING
