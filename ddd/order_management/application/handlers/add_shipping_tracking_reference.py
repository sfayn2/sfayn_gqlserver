from __future__ import annotations
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions


def handle_add_shipping_tracking_reference(
        command: commands.AddShippingTrackingReferenceCommand, 
        uow: UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            order_w_shipping_reference = order.add_shipping_tracking_reference(shipping_reference=command.shipping_reference)


            order_w_shipping_reference_dto =  mappers.OrderResponseMapper.to_dto(
                order=order_w_shipping_reference,
                success=True,
                message="Order successfully added shipping tracking reference."
            )

            uow.order.save(order_w_shipping_reference)
            uow.commit()


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        order_w_shipping_reference_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        order_w_shipping_reference_dto = shared.handle_unexpected_error(f"Unexpected error during add shipping tracking reference {e}")

    return order_w_shipping_reference_dto

