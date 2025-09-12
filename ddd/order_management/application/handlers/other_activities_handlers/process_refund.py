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
            returned_skus = request_return_step.user_input.get("return_skus")

            process_refund_step = order.find_step("process_refund")
            policy = process_refund_step.conditions

            amount = sum(line.total_price.amount for line in self.line_items if line.product_sku in returned_skus),
            amount -= amount * (policy.get("restocking_fee_percent", 0) / 100)


            max_amount = policy.get("max_refund_amount"):
            if max_amount:
                amount = min(amount, max_amount)

            refunded_amount = value_objects.Money(
                amount=amount,
                currency=order.currency
            )

            order.mark_activity_done(
                current_step=command.step_name,
                performed_by=user_ctx.sub,
                user_input={"comments": command.comments, "refunded_amount": refunded_amount }
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully request product return, may subject to approval."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


