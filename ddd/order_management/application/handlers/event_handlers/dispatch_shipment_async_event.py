from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_dispatch_shipment_async_event(
    event: dtos.ConfirmedShipmentIntegrationEvent,
    user_action_service: ports.UserActionServiceAbstract,
    shipping_provider_service: ports.ShippingProviderAbstract,
    uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    with uow:

        data = event.data
        order = uow.order.get(order_id=data.order_id, tenant_id=data.tenant_id)
        shipment = order.get_shipment(shipment_id=data.shipment_id)

        provider_result = shipping_provider_service.create_shipment(data.tenant_id, shipment) 

        user_action_service.save_action(
            dtos.UserActionDTO(
                order_id=data.order_id,
                action="dispatch_shipment",
                performed_by="system",
                user_input=data.dict()
            )
        )

        order.apply_shipment_dispatch(
            data.shipment_id, 
            provider_result.tracking_reference, 
            provider_result.total_amount,
            provider_result.label_url
        )


        uow.order.save(order)
        uow.commit()

        return dtos.ResponseDTO(
            success=True,
            message=f"Dispatched Shipment id {order.order_id} successfully created."
        )
