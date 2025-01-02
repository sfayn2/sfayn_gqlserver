from typing import List
from ddd.order_management.domain.services import shipping_option_handler
from ddd.order_management.domain import enums, models
from django.contrib.auth.models import Group
from django.conf import settings
from decimal import Decimal

class ShippingOptionService(shipping_option_handler.ShippingOptionHandlerMain):

    def __init__(self):
        #check vendor here?
        self.shipping_options = [
            shipping_option_handler.ShippingOptionHandler(
                name=enums.ShippingMethod.STANDARD,
                delivery_time="3-5 business days",
                base_cost=Decimal("5.00")
            ),
            shipping_option_handler.ShippingOptionHandler(
                name=enums.ShippingMethod.EXPRESS,
                delivery_time="1-2 business days",
                base_cost=Decimal("15.00")
            ),
            shipping_option_handler.ShippingOptionHandler(
                name=enums.ShippingMethod.SAME_DAY,
                delivery_time="same day",
                base_cost=Decimal("25.00")
            ),
            shipping_option_handler.ShippingOptionHandler(
                name=enums.ShippingMethod.FLAT_RATE,
                delivery_time="4-6 business days",
                base_cost=Decimal("10.00"),
                flat_rate=Decimal("2.00")
            )
        ]

    def get_shipping_options(self, order: models.Order) -> List[dict]:
        options = []
        for option in self.shipping_options:
            if option.is_eligible(order):
                cost = option.calculate_cost(order)
                options.append({
                    "name": option.name,
                    "delivery_time": option.delivery_time,
                    "cost": cost
                })
        return options