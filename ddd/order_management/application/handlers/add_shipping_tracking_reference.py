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


def handle_add_shipping_tracking_reference(
        command: commands.AddShippingTrackingReferenceCommand, 
        access_control: AccessControlServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="add_shipping_tracking_reference",
                required_scope={"vendor_id": order.vendor_id }
            )

            order.add_shipping_tracking_reference(shipping_reference=command.shipping_reference)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully add shipping tracking reference."
            )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


