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
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="review_order",
                required_scope={"customer_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            escalate_step = order.find_step("escalate_reviewer")

            reviewer = escalate_step.user_input.get("reviewer")
            if user_ctx.sub != reviewer:
                raise exceptions.InvalidOrderOperation("You are not the assigned reviewer.")

            decision = enums.StepOutcome.APPROVED if command.is_approved else enums.StepOutcome.REJECTED

            order.mark_activity_done(
                current_step=command.step_name,
                performed_by=user_ctx.sub,
                user_input={"comments": command.comments},
                outcome=decision
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


