from __future__ import annotations
from typing import Union, Optional
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_review_order(
        command: commands.ReviewOrderCommand, 
        exception_handler: ports.ExceptionHandlerAbstract,
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        user_action_service: ports.UserActionServiceAbstract,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="review_order",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            escalate_step: Optional[dtos.UserActionDTO] = user_action_service.get_last_action(order.order_id, "escalate_reviewer")
            
            if escalate_step is None:
                # Raise a specific domain exception if the required context is missing
                raise exceptions.InvalidOrderOperation("Missing required action 'escalate_reviewer' for reviewing order.")

            reviewer = escalate_step.user_input.get("reviewer")
            if user_ctx.sub != reviewer:
                raise exceptions.InvalidOrderOperation("You are not the assigned reviewer.")


            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=order.order_id,
                    action="review_order",
                    performed_by=user_ctx.sub,
                    user_input={"comments": command.comments},
                )
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

