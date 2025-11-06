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


def handle_confirm_shipment(
        command: commands.ConfirmShipmentCommand, 
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        exception_handler: ExceptionHandlerAbstract,
        user_action_service: UserActionServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="confirm_shipment",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            order.confirm_shipment(shipment_id=command.shipment_id)

            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=command.order_id,
                    action="confirm_shipment",
                    performed_by=user_ctx.sub,
                    user_input=command.model_dump(exclude_none=True)
                )
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} w Shipment Id {command.shipment_id} successfully shipped."
            )


    except exceptions.InvalidOrderOperation as e:
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

