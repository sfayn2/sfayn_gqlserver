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
        uow: UnitOfWorkAbstract,
        access_control_factory: callable[[str], AccessControl1Abstract],
        workflow_service: WorkflowService,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control = access_control_factory(user_ctx.tenant_id)

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="review_order",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            user_action = uow.user_action

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
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


