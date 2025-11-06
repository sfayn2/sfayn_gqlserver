from __future__ import annotations
import uuid
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions


def handle_add_order(
        command: commands.AddOrderCommand, 
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
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
        # Use a WARNING level for handled business exceptions
        logger.warning(
            f"Expected error creating order for user {user_ctx.sub}. Error: {e}",
            exc_info=False # No traceback needed for expected errors
        )
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        # Use an ERROR level for unexpected system crashes, include traceback (exc_info=True)
        logger.error(
            f"UNEXPECTED SYSTEM ERROR during order creation for user {user_ctx.sub}. Error: {e}", 
            exc_info=True 
        )
        return shared.handle_unexpected_error(e)

