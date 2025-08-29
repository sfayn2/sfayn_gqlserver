from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.domain import exceptions
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
    shared
)

def handle_add_line_items(
        command: commands.AddLineItemsCommand, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        stock_validation: StockValidationAbstract,
        access_control: AccessControl1Abstract
) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="add_line_items",
                required_scope={"customer_id": order.customer_details.customer_id}
            )

            stock_validation.ensure_items_in_stock(
                order.tenant_id,
                command.product_skus
            )

            line_items = vendor_repo.get_line_items(
                order.tenant_id,
                command.product_skus
            )

            for line_item in line_items:
                order.add_line_item(line_item)


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully add line items."
            )

    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)



