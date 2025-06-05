from __future__ import annotations
from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared,
    queries
)

def handle_get_order(
        query: queries.OrderQuery, 
        uow: UnitOfWorkAbstract) -> dtos.OrderResponseDTO:
    with uow:

        order = uow.order.get(order_id=query.order_id)

        order_dto =  mappers.OrderResponseMapper.to_dto(
                order=order,
                success=True,
                message="Order successfully query for {query.order_id}."
            )

        return order_dto

