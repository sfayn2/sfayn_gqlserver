from __future__ import annotations
import re
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions
from ddd.order_management.domain.services import DomainClock


def handle_request_return(
        command: commands.RequestReturnCommand, 
        uow: UnitOfWorkAbstract,
        access_control: AccessControl1Abstract,
        workflow_service: WorkflowService,
        user_ctx: dtos.UserContextDTO
) -> dtos.ResponseDTO:

    try:
        with uow:

            access_control.ensure_user_is_authorized_for(
                user_ctx,
                required_permission="request_return",
                required_scope={"role": ["customer"] }
            )

            order = uow.order.get(order_id=command.order_id, tenant_id=user_ctx.tenant_id)

            request_return_step = workflow_service.get_step(order.order_id, "request_return")
            conditions = request_return_step.conditions or {}

            non_returnable_patterns =  conditions.get("non_returnable_sku_patterns", [])
            for sku_pattern in non_returnable_patterns:
                for line in command.product_skus:
                    if re.search(sku_pattern, line.product_sku):
                        raise exceptions.InvalidOrderOperation(
                            f"Returns not allowed for this product sku {line.product_sku}."
                        )


            allow_partial = conditions.get("allow_partial_return", True)
            if allow_partial is False:
                requested_skus = {line.product_sku: line.order_quantity for line in command.product_skus}
                order_line_items = order.get_line_items()

                if set(requested_skus.keys()) != {line.product_sku for line in order_line_items}:
                    raise exceptions.InvalidOrderOperation("Partial return not allowed: missing SKUs.")

                for line in order_line_items:
                    if requested_skus.get(line.product_sku) != line.order_quantity:
                        raise exceptions.InvalidOrderOperation(
                            f"Partial return not allowed: must return fully qty of {line.product_sku}"
                        )
                        

            allowed_days = conditions.get("days_to_return")
            if allowed_days and (DomainClock.now() - order.get_date_modified).days > allowed_days:
                raise exceptions.InvalidOrderOperation("Return window expired")

            workflow_service.mark_step_done(
                order_id=order.order_id,
                current_step=command.step_name,
                performed_by=user_ctx.sub,
                user_input={"comments": command.comments, "return_skus": command.product_skus.model_dump() }
            )


            uow.order.save(order)
            uow.commit()

            return dtos.ResponseDTO(
                success=True,
                message=f"Order {order.order_id} successfully request product return, may be subject to approval."
            )


    except exceptions.InvalidOrderOperation as e:
        return shared.handle_invalid_order_operation(e)
    except Exception as e:
        return shared.handle_unexpected_error(e)


