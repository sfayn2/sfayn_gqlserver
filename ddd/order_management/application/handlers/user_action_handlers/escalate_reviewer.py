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
        access_control_factory: callable[[str], AccessControl1Abstract],
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:
            access_control = access_control_factory(user_ctx.tenant_id)

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="escalate_reviewer",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            user_action = uow.user_action
            user_action.save_action(
                order_id=order.order_id,
                action="escalate_reviewer",
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


