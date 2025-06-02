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


def handle_mark_as_shipped(
        command: commands.MarkAsShippedOrderCommand, 
        uow: UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            shipped_order = order.mark_as_shipped()

            shipped_order_dto =  mappers.OrderResponseMapper.to_dto(
                order=shipped_order,
                success=True,
                message="Order successfully mark as shipped."
            )

            uow.order.save(shipped_order)
            uow.commit()


    except (exceptions.InvalidOrderOperation, ValueError) as e:
        shipped_order_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        shipped_order_dto = shared.handle_unexpected_error(f"Unexpected error during shipped order {e}")

    return shipped_order_dto

