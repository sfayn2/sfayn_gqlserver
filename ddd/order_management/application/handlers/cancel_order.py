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


def handle_cancel_order(
        command: commands.CancelOrderCommand, 
        access_control: AccessControlServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="cancel_order",
                required_scope={"customer_id": order.customer_details.customer_id }
            )

            order.cancel_order(command.cancellation_reason)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully canceled."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

