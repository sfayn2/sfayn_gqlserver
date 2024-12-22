from enum import Enum

class OrderStatus(Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    PAID = "Paid"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)