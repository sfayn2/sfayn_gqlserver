from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions


def handle_place_order(
        command: commands.PlaceOrderCommand, 
        uow: ports.UnitOfWorkAbstract) -> Union[dtos.OrderResponseDTO, dtos.ResponseDTO]:
    try:
        with uow:

            order = mappers.OrderMapper.to_domain(
                uow.order.get(order_id=command.order_id)
            )

            placed_order = order.place_order()
            placed_order_dto =  mappers.OrderResponseMapper.to_dto(
                placed_order
            )

            uow.order.save(placed_order_dto)
            uow.commit()

            placed_order_dto.success = True
            placed_order_dto.message = "Order successfully placed order."

    except (exceptions.InvalidOrderOperation, ValueError) as e:
        placed_order_dto = shared.handle_invalid_order_operation(e)
    except Exception as e:
        placed_order_dto = shared.handle_unexpected_error(f"Unexpected error during place order {e}")

    return placed_order_dto

