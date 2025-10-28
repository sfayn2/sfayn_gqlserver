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


def handle_add_shipment(
        command: commands.AddShipmentCommand, 
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        user_action_service: UserActionServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="add_shipment",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)
            order.create_shipment(
                shipment_address=mappers.AddressDTO.to_domain(command.shipment_address),
                shipment_items=[mappers.ShipmentItemDTO.to_domain(si) for si in command.shipment_items]
            )

            user_action_service.save_action(
                dtos.UserActionDTO(
                    order_id=command.order_id,
                    action="add_shipment",
                    performed_by=user_ctx.sub,
                    user_input=command.model_dump(exclude_none=True)
                )
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully add new shipment."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

