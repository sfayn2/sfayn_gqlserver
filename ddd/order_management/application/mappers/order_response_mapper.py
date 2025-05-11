from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models

class OrderResponseMapper:

    @staticmethod
    def to_dto(order: models.Order, success: bool = True, message: str = None) -> dtos.OrderResponseDTO:
        response_dto = dtos.OrderResponseDTO(
                order_id=order.order_id,
                order_status=order.order_status,
                success=success,
                message=message,
                tax_details=order.tax_details,
                offer_details=order.offer_details,
                shipping_details=asdict(order.shipping_details) if order.shipping_details else None,
                tax_amount=asdict(order.tax_amount),
                total_discounts_fee=asdict(order.total_discounts_fee),
                final_amount=asdict(order.final_amount)
            )
        return response_dto