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
        stock_validation_service: StockValidationServiceAbstract
    ) -> dtos.ResponseDTO:
    try:
        with uow:

            order = uow.order.get(order_id=command.order_id)
            order.change_order_quantity(
                product_sku=command.product_sku,
                new_quantity=command.new_quantity
            )

            stock_validation_service.ensure_items_in_stock(order.line_items)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully changed order quantity of Produt SKU {command.product_sku}."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)
