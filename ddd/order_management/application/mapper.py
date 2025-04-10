from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class OrderResponseMapper:

    @classmethod
    def to_dto(cls, order: models.Order, success: bool = True, message: str = None) -> dtos.OrderResponseDTO:
        response_dto = dtos.OrderResponseDTO(
                order_id=order.order_id,
                order_status=order.order_status,
                success=success,
                message=message,
                tax_details=order.tax_details,
                offer_details=order.offer_details,
                shipping_details=asdict(order.shipping_details),
                tax_amount=asdict(order.tax_amount),
                total_discounts_fee=asdict(order.total_discounts_fee),
                final_amount=asdict(order.final_amount)
            )
        return response_dto

class ShippingDetailsMapper:

    @classmethod
    def from_domain(cls, shipping_details: value_objects.ShippingDetails) -> dtos.ShippingDetailsDTO:
        return dtos.ShippingDetailsDTO(**asdict(shipping_details))


class ShippingOptionsResponseMapper:

    @classmethod
    def to_dtos(cls, shipping_options: List[value_objects.ShippingDetails]) -> List[dtos.ShippingDetailsDTO]:
        return [ShippingDetailsMapper.from_domain(option) for option in shipping_options]

