
from enum import IntEnum

class DeliveryStatus(IntEnum):
    PENDING_ACCEPTANCE = 4
    PICKUP_IN_PROGRESS = 5
    PICKED = 6
    ITEM_PICKED_UP = 7
    DELIVERED = 8
    UNDELIVERED = 9

