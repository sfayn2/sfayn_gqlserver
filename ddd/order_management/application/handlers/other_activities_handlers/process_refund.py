from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import (
    exceptions,
    value_objects
)
from ddd.order_management.domain.services import DomainClock


def handle_process_refund(
        command: commands.ProcessRefundCommand, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="process_refund",
                required_scope={"vendor_id": user_ctx.sub }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            request_return_step = order.find_step("request_return")
            returned_skus = request_return_step.user_input.get("return_skus", [])

            process_refund_step = order.find_step("process_refund")
            conditions = process_refund_step.conditions or {}

            returned_sku_set = {
                sku["product_sku"]:sku["order_quantity"] 
                for sku in returned_skus
            }

            amount = sum(
                li.product_price.amount * min(returned_sku_set[li.product_sku], li.order_quantity) 
                for li in order.get_line_items() 
                if li.product_sku in returned_sku_set.keys()
            )

            restocking_fee_percent = conditions.get("restocking_fee_percent", 0)
            if restocking_fee_percent > 0:
                amount -= amount * (restocking_fee_percent / 100)


            max_amount = conditions.get("max_refund_amount")
            if max_amount is not None:
                amount = min(amount, max_amount)

            refunded_amount = value_objects.Money(
                amount=amount,
                currency=order.currency
            )

            order.mark_activity_done(
                current_step=command.step_name,
                performed_by=user_ctx.sub,
                user_input={"comments": command.comments, "refunded_amount": refunded_amount.as_dict() }
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully processed refund."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


