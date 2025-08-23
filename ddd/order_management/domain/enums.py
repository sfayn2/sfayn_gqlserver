from enum import Enum

def generate_choices(cls):
    #TODO not applicable anymore since key value matches
    return tuple((i.value, i.name.replace("_"," ").title()) for i in cls)


class OrderStatus(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

    @classmethod
    def choices(cls):
        return generate_choices(cls)


class ShippingMethod(Enum):
    STANDARD = "STANDARD"
    EXPRESS = "EXPRESS"
    LOCAL_PICKUP = "LOCAL_PICKUP"
    FREE_SHIPPING = "FREE_SHIPPING"
    SAME_DAY = "SAME_DAY_DELIVERY"
    FLAT_RATE = "FLAT_RATE"
    OTHER = "OTHER" # for custom or external shipping method?

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class OfferType(Enum):
    PERCENTAGE_DISCOUNT = "PERCENTAGE_DISCOUNT"
    FIXED_DISCOUNT = "FIXED_DISCOUNT"
    COUPON_PERCENTAGE_DISCOUNT = "COUPON_PERCENTAGE_DISCOUNT"
    BUNDLE = "BUNDLE"
    FREE_GIFTS = "FREE_GIFTS"
    FREE_SHIPPING = "FREE_SHIPPING"
    OTHER = "OTHER" # for custom 

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class PaymentMethod(Enum):
    DIGITAL_WALLET = "DIGITAL_WALLET"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"
    OTHER = "OTHER" # for custom 

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class PaymentStatus(Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class TaxType(Enum):
    SALES_TAX = "SALES_TAX"
    STATE_TAX = "STATE_TAX"
    VAT = "VAT"
    GST = "GST"
    NONE = "NONE" # explicitly no tax
    OTHER = "OTHER"

    @classmethod
    def choices(cls):
        return generate_choices(cls)