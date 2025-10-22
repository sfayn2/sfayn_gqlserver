from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions
from ddd.order_management.domain.services import DomainClock


def handle_request_return(
        command: commands.RequestReturnCommand, 
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
                required_permission="request_return",
                required_scope={"role": ["customer"] }
            )

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully request product return, may be subject to approval."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


