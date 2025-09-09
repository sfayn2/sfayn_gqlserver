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


def handle_escalate_reviewer(
        command: commands.EscalateReviewerCommand, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="escalate_reviewer",
                required_scope={"customer_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            order.mark_activity_done(
                current_step=command.step_name,
                performed_by=user_ctx.sub,
                user_input={"reviewer": command.reviewer, "comments": command.comments }
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully escalate to reviewer."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


