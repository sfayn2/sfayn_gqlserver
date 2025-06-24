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

def handle_confirm_order(
        command: commands.ConfirmOrderCommand, 
        uow: UnitOfWorkAbstract, 
        payment_service: PaymentServiceAbstract,
        stock_validation_service: StockValidationServiceAbstract
    ) -> dtos.ResponseDTO:

    try:

        with uow:

            order = uow.order.get(order_id=command.order_id)

            stock_validation_service.ensure_items_in_stock(order.line_items)

            payment_gateway = payment_service.get_payment_gateway(command.payment_method)
            payment_details = payment_gateway.get_payment_details(
                command.transaction_id,
                order=order
            )

            is_payment_verified = order.verify_payment(
                payment_details
            )

            order.confirm_order(is_payment_verified)

            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully confirmed."
            )
    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)

