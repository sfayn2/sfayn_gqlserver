from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import (
    exceptions,
    value_objects
)
from ddd.order_management.domain.services import DomainClock


def handle_process_refund(
        command: commands.ProcessRefundCommand, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract,
        refund_service: RefundService,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="process_refund",
                required_scope={"role": ["vendor"] }
            )

            refund_service.process_refund(
                order_id=commands.order_id, 
                tenant_id=user_ctx.tenant_id,
                performed_by=user_ctx.sub,
                comments=commands.comments
            )


            return dtos.ResponseDTO(
                success=True,
                message=f"Order {commands.order_id} successfully processed refund."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


