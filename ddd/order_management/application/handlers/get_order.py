from __future__ import annotations
from typing import Union, List
from ddd.order_management.application import (
    mappers, 
    ports, 
    dtos, 
    queries
)

def handle_get_order(
        query: queries.GetOrderQuery, 
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        uow: ports.UnitOfWorkAbstract) -> dtos.OrderResponseDTO:

    access_control.ensure_user_is_authorized_for(
        user_ctx,
        required_permission="get_order",
        required_scope={"customer_id": user_ctx.sub }
    )

    order = uow.order.get(order_id=query.order_id, tenant_id=user_ctx.tenant_id)

    return dtos.OrderResponseDTO(
        **mappers.OrderMapper.to_dto(
            order=order
        ).model_dump()
    )


