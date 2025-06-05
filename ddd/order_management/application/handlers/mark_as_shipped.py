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
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)
            order.mark_as_shipped()

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message="Cart items successfully mark as shipped."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

