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
        exception_handler: ports.ExceptionHandlerAbstract,
        user_action_service: ports.UserActionServiceAbstract,
        uow: ports.UnitOfWorkAbstract) -> dtos.OrderResponseDTO:


    access_control.ensure_user_is_authorized_for(
        user_ctx,
        required_permission="get_order",
        required_scope={"role": ["vendor"] }
    )

    order = uow.order.get(order_id=query.order_id, tenant_id=user_ctx.tenant_id)

    # GraphQl Object Type already control fields to return
    return mappers.OrderMapper.to_response_dto(
            order=order
        )

    #return order


