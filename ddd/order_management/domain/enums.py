from enum import Enum

def generate_choices(cls):
    #TODO not applicable anymore since key value matches
    return tuple((i.value, i.name.replace("_"," ").title()) for i in cls)

class OrderStatus(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PARTIAL_SHIPPED = "PARTIAL_SHIPPED"
    SHIPPED = "SHIPPED"
    PARTIAL_DELIVERED = "PARTIAL_DELIVERED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class PaymentStatus(Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class ShipmentStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class ShipmentMethod(Enum):
    PICKUP = "PICKUP"
    DROPOFF = "DROPOFF"
    WAREHOUSE = "WAREHOUSE"
