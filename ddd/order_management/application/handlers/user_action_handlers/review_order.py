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


def handle_review_order(
        command: commands.ReviewOrderCommand, 
        uow: ports.UnitOfWorkAbstract,
        exception_handler: ports.ExceptionHandlerAbstract,
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="review_order",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            user_action = uow.user_action
            #TODO

            escalate_step = user_action.get(order.order_id, "escalate_reviewer")

            reviewer = escalate_step.user_input.get("reviewer")
            if user_ctx.sub != reviewer:
                raise exceptions.InvalidOrderOperation("You are not the assigned reviewer.")


            user_action.save_action(
                order_id=order.order_id,
                action="review_order",
                performed_by=user_ctx.sub,
                user_input={"comments": command.comments},
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully reviewed."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

