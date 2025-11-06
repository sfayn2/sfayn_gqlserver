from __future__ import annotations
import uuid
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_add_order(
        command: commands.AddOrderCommand, 
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        exception_handler: ExceptionHandlerAbstract,
        user_action_service: UserActionServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="add_order",
                required_scope={"role": ["vendor"] }
            )

            
            order = uow.order.create_order(
                customer_details=mappers.CustomerDetailsMapper.to_domain(command.customer_details),
                line_items=[mappers.LineItemMapper.to_domain(sku) for sku in command.product_skus],
                tenant_id=user_ctx.tenant_id
            )


            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=order.order_id,
                    action="add_order",
                    performed_by=user_ctx.sub,
                    user_input=command.model_dump(exclude_none=True)
                )
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order successfully created."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

