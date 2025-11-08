from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_request_return(
        command: commands.RequestReturnCommand, 
        exception_handler: ports.ExceptionHandlerAbstract,
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="request_return",
                required_scope={"role": ["customer"] }
            )

            return dtos.ResponseDTO(
                success=True,
                message=f"Order successfully request product return, may be subject to approval."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

