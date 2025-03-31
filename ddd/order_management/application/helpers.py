from dataclasses import asdict
from typing import List
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, enums, value_objects
from ddd.order_management.infrastructure import logging, order_dtos

logger = logging.get_logger(__name__)

def handle_invalid_order_operation(err):
    logger.error(f"{err}")
    response_dto = dtos.ResponseDTO(
        success=False,
        message=str(err)
    )
    return response_dto

def handle_unexpected_error(err_details):
    logger.error(f"{err_details}", exc_info=True)
    response_dto = dtos.ResponseDTO(
        success=False,
        message="An unexpected error occured. Please contact support."
    )
    return response_dto

def get_order_response_dto(order: models.Order, success: bool = True, message: str = None):
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

def get_shipping_options_response_dto(shipping_options: List[value_objects.ShippingDetails]) -> List[order_dtos.ShippingDetailsDTO]:
    response_dtos = []
    for option in shipping_options:
        response_dtos.append(
            order_dtos.ShippingDetailsDTO.from_domain(option)
        )
    return response_dtos

    

