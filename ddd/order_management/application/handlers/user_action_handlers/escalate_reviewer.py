from __future__ import annotations
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_escalate_reviewer(
        command: commands.EscalateReviewerCommand, 
        exception_handler: ports.ExceptionHandlerAbstract,
        access_control: ports.AccessControl1Abstract,
        user_action_service: ports.UserActionServiceAbstract,
        user_ctx: dtos.UserContextDTO,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="escalate_reviewer",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=order.order_id,
                    action="escalate_reviewer",
                    performed_by=user_ctx.sub,
                    user_input={"reviewer": command.reviewer, "comments": command.comments }
                )
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully escalate to reviewer."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)