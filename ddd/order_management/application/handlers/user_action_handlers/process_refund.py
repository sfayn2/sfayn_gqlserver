from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_process_refund(
        command: commands.ProcessRefundCommand, 
        refund_service: ports.RefundService,
        exception_handler: ports.ExceptionHandlerAbstract,
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="process_refund",
                required_scope={"role": ["vendor"] }
            )

            refund_service.process_refund(
                order_id=command.order_id, 
                tenant_id=user_ctx.tenant_id,
                performed_by=user_ctx.sub,
                comments=command.comments
            )


            return dtos.ResponseDTO(
                success=True,
                message=f"Order {command.order_id} successfully processed refund."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)
