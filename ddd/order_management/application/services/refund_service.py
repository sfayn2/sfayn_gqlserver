from __future__ import annotations
from ddd.order_management.domain import value_objects

class RefundService:
    def __init__(self, 
        uow: UnitOfWorkAbstract, 
        tenant_service: TenantServiceAbstract, 
        user_action_service: UserActionServiceAbstract):
        self.uow = uow
        self.tenant_service = tenant_service
        self.user_action_service = user_action_service

    def process_refund(self, 
        order_id: str, 
        tenant_id: str, 
        comments: str, 
        action: str = "process_refund"
    ):
        order = self.uow.order.get(order_id=order_id, tenant_id=tenant_id)
        tenant_config = tenant_service.get_tenant_config(tenant_id)

        request_return_step = user_action_service.get_last_action(order_id, "request_return")
        returned_skus = request_return_step.user_input.get("return_skus", [])

        returned_sku_set = {
            sku["product_sku"]:sku["order_quantity"] 
            for sku in returned_skus
        }

        amount = sum(
            li.product_price.amount * min(returned_sku_set[li.product_sku], li.order_quantity) 
            for li in order.get_line_items() 
            if li.product_sku in returned_sku_set.keys()
        )

        restocking_fee_percent = tenant_config.get("restocking_fee_percent", 0)
        if restocking_fee_percent > 0:
            amount -= amount * (restocking_fee_percent / 100)


        max_amount = tenant_config.get("max_refund_amount")
        if max_amount is not None:
            amount = min(amount, max_amount)

        refunded_amount = value_objects.Money(
            amount=amount,
            currency=order.currency
        )

        user_action_data = dtos.UserActionDTO(
                order_id=order_id,
                action=action,
                performed_by=performed_by,
                user_input={"comment": comments, "refunded_amount": refunded_amount.as_dict() }
            )

        user_action_service.save_action(
            user_action_data
        )


        self.uow.order.save(order)
        self.uow.commit()