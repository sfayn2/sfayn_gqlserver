from __future__ import annotations
from typing import Union, TYPE_CHECKING
from ddd.order_management.domain import exceptions
from ddd.order_management.application import (
    mappers, 
    commands, 
    dtos, 
    shared
)

def handle_add_line_item(
        command: commands.AddLineItemCommand, 
        uow: UnitOfWorkAbstract,
        vendor_repo: VendorAbstract,
        stock_validation_service: StockValidationServiceAbstract
) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)

            line_items = vendor_repo.get_line_items(
                order.vendor_id, 
                [command.product_sku]
            )

            # we expect single return here; then why do we loop?
            for line_item in line_items:
                order.add_line_item(line_item)

            stock_validation_service.ensure_items_in_stock(order.line_items)

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



