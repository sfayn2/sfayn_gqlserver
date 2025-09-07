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
        command: commands.ShipOrderCommand, 
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="mark_as_shipped",
                required_scope={"vendor_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            order.mark_activity_done(
                command.step_name,
                user_ctx.sub
            )
            order.mark_as_shipped()

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully mark as shipped."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

