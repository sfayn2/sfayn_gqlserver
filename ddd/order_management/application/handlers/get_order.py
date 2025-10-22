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
        access_control_factory: callable[[str], AccessControl1Abstract],
        user_ctx: dtos.UserContextDTO,
        uow: UnitOfWorkAbstract) -> dtos.OrderResponseDTO:

    access_control = access_control_factory(user_ctx.tenant_id)

    access_control.ensure_user_is_authorized_for(
        user_ctx,
        required_permission="get_order",
        required_scope={"customer_id": user_ctx.sub }
    )

    order = uow.order.get(order_id=query.order_id, tenant_id=user_ctx.tenant_id)

    return mappers.OrderMapper.to_dto(
            order=order
        )

