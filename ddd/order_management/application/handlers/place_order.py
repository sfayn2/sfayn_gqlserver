from __future__ import annotations
from typing import Union, TYPE_CHECKING
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
        stock_validation_service: StockValidationServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)
            stock_validation_service.ensure_items_in_stock(order.line_items)
            order.place_order()

            uow.order.save(order)
            uow.commit()

            #TODO to check if commit is really success
            return dtos.ResponseDTO(
                success=True,
                message="Order successfully placed order."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

