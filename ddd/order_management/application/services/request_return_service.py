from __future__ import annotations
from ddd.order_management.domain import value_objects

class RequestReturnService:
    def __init__(self, uow: UnitOfWorkAbstract):
        self.uow = uow

    def request_return(self, order_id: str, tenant_id: str, comments: str, action: str = "process_refund"):
        order = uow.order.get(order_id=order_id, tenant_id=tenant_id)

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
