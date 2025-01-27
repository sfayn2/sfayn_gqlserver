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
    SAME_DAY = "Same Day Delivery"
    FLAT_RATE = "Flat Rate"

    @classmethod
    def choices(cls):
        return generate_choices(cls)

class OfferType(Enum):
    PERCENTAGE_DISCOUNT = "Percentage Discount"
    FIXED_DISCOUNT = "Fixed Discount"
    COUPON_DISCOUNT = "Coupon Percentage Discount"
    BUNDLE = "Bundle"
    FREE_GIFT = "Free Gift"
    FREE_SHIPPING = "Free Shipping"

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