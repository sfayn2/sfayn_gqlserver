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

class ShippingMethod(Enum):
    STANDARD = "Standard"
    EXPRESS = "Express"
    SAME_DAY = "Same Day Delivery"
    FLAT_RATE = "Flat Rate"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class OfferType(Enum):
    DISCOUNT = "Discount"
    BUNDLE = "Bundle"
    FREE_GIFT = "Free Gift"
    FREE_SHIPPING = "Free Shipping"

class DiscountType(Enum):
    PERCENTAGE = "Percentage"
    FIXED_AMOUNT = "Fixed Amount"

class PaymentMethod(Enum):
    PAYPAL = "Paypal"
    STRIPE = "Stripe"
    COD = "Cash On Delivery"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)