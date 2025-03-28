from enum import Enum

def generate_choices(cls):
    return tuple((i.value, i.name.replace("_"," ").title()) for i in cls)


class OrderStatus(Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return generate_choices(cls)


class ShippingMethod(Enum):
    STANDARD = "Standard"
    EXPRESS = "Express"
    LOCAL_PICKUP = "Local Pickup"
    FREE_SHIPPING = "Free Shipping"
    SAME_DAY = "Same Day Delivery"
    FLAT_RATE = "Flat Rate"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class OfferType(Enum):
    PERCENTAGE_DISCOUNT = "percentage_discount"
    FIXED_DISCOUNT = "fixed_discount"
    COUPON_PERCENTAGE_DISCOUNT = "coupon_discount"
    BUNDLE = "bundle"
    FREE_GIFT = "free_gift"
    FREE_SHIPPING = "free_shipping"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class PaymentMethod(Enum):
    PAYPAL = "Paypal"
    STRIPE = "Stripe"
    COD = "Cash On Delivery"

    @classmethod
    def choices(cls):
        return generate_choices(cls)