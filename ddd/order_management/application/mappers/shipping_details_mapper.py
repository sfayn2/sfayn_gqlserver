from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class ShippingDetailsMapper:

    @staticmethod
    def to_dto(shipping_details: value_objects.ShippingDetails) -> dtos.ShippingDetailsDTO:
        return dtos.ShippingDetailsDTO(**asdict(shipping_details))

    @staticmethod
    def to_domain(shipping_details_dto: dtos.ShippingDetailsDTO) -> value_objects.ShippingDetails:
        return value_objects.ShippingDetails(
            method=enums.ShippingMethod(shipping_details_dto.method),
            delivery_time=shipping_details_dto.delivery_time,
            cost=value_objects.Money(
                amount=shipping_details_dto.cost.amount,
                currency=shipping_details_dto.cost.currency
            )
        )

