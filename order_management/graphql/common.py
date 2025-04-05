import graphene
from graphene import relay
from dataclasses import asdict
from typing import List
from order_management.graphql import object_types, input_types
from ddd.order_management.application import (
    message_bus, unit_of_work, dtos
  )
from ddd.order_management.domain import exceptions
from ddd.order_management.infrastructure import logging, order_dtos
from ddd.order_management.domain import models, value_objects

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
    return [order_dtos.ShippingDetailsDTO.from_domain(option) for option in shipping_options]


class BaseMutation(relay.ClientIDMutation):
    order = graphene.Field(object_types.OrderResponseType)

    command_class = None
    success_message = None
    exception_message = None

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = cls.PlaceOrderCommand.model_validate(input)
            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())
            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order
            response_dto = get_order_response_dto(order, success=True, message=cls.success_message)

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = handle_unexpected_error(f"{cls.exception_message} {e}")

        return cls(order=object_types.OrderResponseType(**response_dto.model_dump()))