from __future__ import annotations
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
)
from ddd.order_management.domain import exceptions


def handle_add_shipment(
        command: commands.AddShipmentCommand, 
        access_control: ports.AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO,
        exception_handler: ports.ExceptionHandlerAbstract,
        user_action_service: ports.UserActionServiceAbstract,
        uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:
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
                shipment_items=[mappers.ShipmentItemDTO.to_domain(si, order.get_line_item(si.product_sku, si.vendor_id)) for si in command.shipment_items]
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
        # Delegate handling of EXPECTED exceptions to the infrastructure service
        return exception_handler.handle_expected(e)
    except Exception as e:
        # Delegate handling of UNEXPECTED exceptions to the infrastructure service
        return exception_handler.handle_unexpected(e)

