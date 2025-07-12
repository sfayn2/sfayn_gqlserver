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
        access_control: AccessControlServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.OrderResponseDTO:

    order = uow.order.get(order_id=query.order_id)

    access_control.ensure_user_is_authorized_for(
        token=command.token,
        required_permission="get_order",
        required_scope={"customer_id": order.customer_details.customer_id }
    )

    return mappers.OrderMapper.to_dto(
            order=order
        )

