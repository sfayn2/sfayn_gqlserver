import ast
from ddd.order_management.domain import models, value_objects, enums

class ShippingDetailsMapper:

    @staticmethod
    def to_domain(shipping_details_object) -> value_objects.ShippingDetails:
        return value_objects.ShippingDetails(
                method=enums.ShippingMethod(shipping_details_object.shipping_method),
                delivery_time=shipping_details_object.shipping_delivery_time,
                cost=value_objects.Money(
                    amount=shipping_details_object.shipping_cost,
                    currency=shipping_details_object.currency
                )
            )