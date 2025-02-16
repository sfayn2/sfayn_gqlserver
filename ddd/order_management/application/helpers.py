from ddd.order_management.application import dtos
from ddd.order_management.infrastructure import logging

logger = logging.get_logger(__name__)

def handle_invalid_order_operation(err):
    logger.error(f"{err}")
    response_dto = dtos.ResponseWExceptionDTO(
        success=False,
        message=str(err)
    )
    return response_dto

def handle_unexpected_error(err_details):
    logger.error(f"{err_details}", exc_info=True)
    response_dto = dtos.ResponseWExceptionDTO(
        success=False,
        message="An unexpected error occured. Please contact support."
    )