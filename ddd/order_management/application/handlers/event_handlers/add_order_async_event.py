from __future__ import annotations
import json
from ddd.order_management.application import (
    mappers,
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions, models

def handle_add_order_async_event(
    event: dtos.AddOrderIntegrationEvent,
    user_action_service: ports.UserActionServiceAbstract,
    uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    with uow:

        data = event.data
        order = models.Order.create_order(
            customer_details=mappers.CustomerDetailsMapper.to_domain(data.customer_details),
            line_items=[mappers.LineItemMapper.to_domain(sku) for sku in data.product_skus],
            tenant_id=data.tenant_id,
            external_ref=data.external_ref
        )


        user_action_service.save_action(
            dtos.UserActionDTO(
                order_id=order.order_id,
                action="add_order",
                performed_by="system",
                user_input=data.dict()
            )
        )

        uow.order.save(order)
        uow.commit()

        return dtos.ResponseDTO(
            success=True,
            message=f"Order {order.order_id} successfully created."
        )


