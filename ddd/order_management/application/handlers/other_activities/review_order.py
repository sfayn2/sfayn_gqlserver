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
        access_control: AccessControl1Abstract
) -> dtos.ResponseDTO:

    try:
        with uow:

            user_ctx = access_control.get_user_context(command.token)
            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="review_order",
                required_scope={"customer_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            #find escalate step
            escalate_step = next(
                (a for a in order.activities is a.step_name == "escalate_reviewer"),
                None
            )
            if not escalate_step or escalate_step.is_pending():
                raise exceptions.InvalidOrderOperation("Order has not been escalated yet.")

            reviewer = escalate_step.user_input.get("reviewer")
            if user_ctx.sub != reviewer:
                raise exceptions.InvalidOrderOperation("You are not the assigned reviewerOrder has not been escalated yet..")

            if command.is_approved = True:
                decision = enums.StepOutcome.APPROVED
            else
                decision = enums.StepOutcome.REJECTED

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
                message=f"Order {order.order_id} successfully review order."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


