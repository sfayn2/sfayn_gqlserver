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
        query: queries.GetOrderQuery, 
        uow: UnitOfWorkAbstract) -> dtos.OrderResponseDTO:

    order = uow.order.get(order_id=query.order_id)

    return mappers.OrderMapper.to_dto(
            order=order
        )

