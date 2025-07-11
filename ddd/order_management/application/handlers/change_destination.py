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


def handle_change_destination(
        command: commands.ChangeDestinationCommand, 
        uow: UnitOfWorkAbstract,
        validation_service: CustomerAddressValidationAbstract
    ) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            # Decision: allow to change w adhoc address
            #validation_service.ensure_customer_address_is_valid(
            #    customer_id=order.customer_details.customer_id,
            #    address=command.address
            #)

            order.change_destination(
                command.address
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully changed destination."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

