from __future__ import annotations
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    services as application_services,
    shared
)
from ddd.order_management.domain import exceptions

def handle_confirm_order(
        command: commands.ConfirmOrderCommand, 
        uow: UnitOfWorkAbstract, 
        payment_service: application_services.PaymentService,
        access_control: AccessControl1Abstract,
        stock_validation: StockValidationAbstract
    ) -> dtos.ResponseDTO:

    try:

        with uow:

            order = uow.order.get(order_id=command.order_id)

            access_control.ensure_user_is_authorized_for(
                token=command.token,
                required_permission="confirm_order",
                required_scope={"customer_id": order.customer_details.customer_id }
            )

            stock_validation.ensure_items_in_stock(
                order.tenant_id,
                order.line_items
            )

            payment_option = payment_service.select_payment_option(command.payment_method, command.provider)
            payment_details = payment_option.get_payment_details(
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

