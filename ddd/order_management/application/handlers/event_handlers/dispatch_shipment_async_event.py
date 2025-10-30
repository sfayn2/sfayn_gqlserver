from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_dispatch_shipment_async_event(
    event: dtos.ConfirmedShipmentIntegrationEvent,
    user_action_service: UserActionServiceAbstract,
    shipping_provider_service: ports.ShippingProviderAbstract,
    uow: UnitOfWorkAbstract) -> dtos.ResponseDTO:

    with uow:

        order = uow.order.get(order_id=event.order_id, tenant_id=event.tenant_id)
        shipment = order.get_shipment(shipment_id=event.shipment_id)

        provider_result = shipping_provider_service.create_shipment(tenant_id, shipment) 

        shipment.update_tracking_reference(provider_result.tracking_reference)
        shipment.update_shipping_amount(provider_result.total_amount)

        user_action_service.save_action(
            dtos.UserActionDTO(
                order_id=event.order_id,
                action="dispatch_shipment",
                performed_by="system",
                user_input=event.dict()
            )
        )

        uow.order.save(order)
        uow.commit()

        print(f"Dispatched Shipment id {event.shipment_id}")
