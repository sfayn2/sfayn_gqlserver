from enum import Enum

def generate_choices(cls):
    #TODO not applicable anymore since key value matches
    return tuple((i.value, i.name.replace("_"," ").title()) for i in cls)

class StepOutcome(Enum):
    WAITING = "WAITING"
    DONE = "DONE"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    #SKIPPED = "SKIPPED"

    @classmethod
    def choices(cls):
        return generate_choices(cls)


class OrderStage(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class PaymentStatus(Enum):
    PAID = "PAID"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class ShipmentStatus(Enum):
    DELIVERED = "DELIVERED"
    SHIPPED = "SHIPPED"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return generate_choices(cls)
