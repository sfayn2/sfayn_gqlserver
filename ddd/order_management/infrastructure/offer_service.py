from ddd.order_management.domain.services import offer_handler
from ddd.order_management.domain import models, enums, value_objects
from decimal import Decimal

enums.OfferType.PERCENTAGE_DISCOUNT
class OfferService(offer_handler.OfferHandlerMain):

    def __init__(self):
        #To get from Vendor management config?
        self.offer_handlers = [
            offer_handler.DiscountOfferHandler(
                offer_type=enums.OfferType.PERCENTAGE_DISCOUNT,
                description="10% off Lacoste Product",
                discount_value=Decimal("10"),
                condition={ 
                    "eligible_products": ["Lacoste"],
                },
                start_date="12/31/2024",
                end_date="12/31/2025"
            ),
            offer_handler.DiscountCouponOfferHandler(
                offer_type=enums.OfferType.PERCENTAGE_DISCOUNT,
                description="10% off w WELCOME25",
                discount_value=Decimal("10"),
                condition={
                    "eligible_products": ["Lacoste"],
                    "requires_coupon": True,
                    "coupon_code": "WELCOME25",
                },
                start_date="12/31/2024",
                end_date="12/31/2025"
            ),
            offer_handler.FreeGiftOfferHandler(
                offer_type=enums.OfferType.FREE_GIFT,
                description="Free gift for 2+ items",
                condition={
                    "minimum_quantity": 2,
                    "gift_products": [{"sku": "T-SH-XL", "quantity": 1}]
                },
                start_date="12/31/2024",
                end_date="12/31/2025"
            ),
            offer_handler.FreeShippingOfferHandler(
                offer_type=enums.OfferType.FREE_SHIPPING,
                description="Free shipping for orders above $150",
                condition={
                    "minimum_order_total": 150,
                    "start_date": "12/31/2024",
                    "end_date": "12/31/2025",
                },
                start_date="12/31/2024",
                end_date="12/31/2025"
            )

        ]

    def apply_offers(self, order: models.Order):
        offer_details = []

        for offer_handler in self.offer_handlers:
            offer_details.append(
                offer_handler.apply_offer(order)
            )

        order.update_offer_details(offer_details)

