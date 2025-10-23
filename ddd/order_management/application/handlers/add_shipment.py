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
from ddd.order_management.domain import exceptions, value_objects, model


def handle_add_shipment(
        command: commands.AddShipmentCommand, 
        access_control_factory: callable[[str], AccessControl1Abstract],
        user_ctx: dtos.UserContextDTO,
        user_action_service: UserActionServiceAbstract,
        uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:
    try:
        with uow:
            access_control = access_control_factory(user_ctx.tenant_id)

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="add_shipment",
                required_scope={"role": ["vendor"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            shipment = model.Shipment(
                shipment_id=command.shipment_id,
                shipment_address=value_objects.Address(**command.shipment_address),
                shipment_amount=value_objects.Money(
                    amount=command.shipment_amount,
                    currency=command.shipment_amount_currency
                ),
                shipment_tax_amount=value_objects.Money(
                    amount=command.shipment_amount,
                    currency=command.shipment_amount_currency
                ),
                shipment_items=[]
            )

            for item_data in command.shipment_items:
                line_item = order.get_line_item(item_data.product_sku, item_data.vendor_id)
                shipment_item = model.ShipmentItem(
                    shipment_item_id=str(uuid.uuid4()),
                    line_item=line_item,
                    quantity=item_data.quantity
                )
                shipment.add_line_item(shipment_item)

            shipment.allocation_shipping_tax()
            order.add_shipment(shipment)

            user_action_data = dtos.UserActionDTO(
                    order_id=command.order_id,
                    action="add_shipment",
                    performed_by=user_ctx.sub,
                    user_input={}
                )

            user_action_service.save_action(
                user_action_data
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

