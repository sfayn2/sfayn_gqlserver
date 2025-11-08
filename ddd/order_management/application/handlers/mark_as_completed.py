from __future__ import annotations
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_mark_as_completed(
        command: commands.CompleteOrderCommand, 
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        exception_handler: ports.ExceptionHandlerAbstract,
        user_action_service: ports.UserActionServiceAbstract,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="mark_as_completed",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            order.mark_as_completed()

            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=command.order_id,
                    action="mark_as_completed",
                    performed_by=user_ctx.sub,
                    user_input=command.model_dump(exclude_none=True)
                )
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully mark as completed."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)




