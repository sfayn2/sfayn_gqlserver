from ddd.order_management.infrastructure.adapters import unit_of_work
import graphene
from graphene import relay
from dataclasses import asdict
from typing import List
from order_management.graphql import object_types, input_types
from ddd.order_management.application import (
    message_bus, dtos, mapper
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




class BaseOrderMutation(relay.ClientIDMutation):
    order = graphene.Field(object_types.OrderResponseType)

    command_class = None
    exception_message = None
    dependencies = None

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = cls.command_class.model_validate(input)
            response_dto = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork(), dependencies=cls.dependencies)
            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = handle_unexpected_error(f"{cls.exception_message} {e}")

        return cls(order=object_types.OrderResponseType(**response_dto.model_dump()))
