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


def handle_change_order_quantity(
        command: commands.ChangeOrderQuantityCommand, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract,
        stock_validation: StockValidationAbstract,
        user_ctx: dtos.UserContextDTO
    ) -> dtos.ResponseDTO:
    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="change_order_quantity",
                required_scope={"customer_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            for sku in command.product_skus:
                order.change_order_quantity(
                    product_sku=sku.product_sku,
                    new_quantity=sku.order_quantity
                )

            stock_validation.ensure_items_in_stock(
                order.tenant_id,
                command.product_skus
            )

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully changed order quantity of Product SKU {','.join([sku.product_sku for sku in command.product_skus])}."

            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)
