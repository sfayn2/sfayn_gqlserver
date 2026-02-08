from __future__ import annotations
import json
from ddd.order_management.application import (
    mappers,
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_shipping_provider_create_shipment_async_event(
    event: dtos.ConfirmedShipmentIntegrationEvent,
    user_action_service: ports.UserActionServiceAbstract,
    shipping_provider_service: ports.ShippingProviderServiceAbstract,
    uow: ports.UnitOfWorkAbstract) -> dtos.ResponseDTO:

    with uow:
        data = event.data
        order = uow.order.get(order_id=data.order_id, tenant_id=data.tenant_id)
        shipment = order.get_shipment_by_id(data.shipment_id)
        
        # 1. Integration Call (WSS/EasyPost/Self Delivered)
        provider_result = shipping_provider_service.create_shipment(data.tenant_id, shipment)

        # 2. Attach Data to Domain (Shipment Status stays CONFIRMED)
        order.apply_fulfillment_data(
            shipment_id=data.shipment_id,
            tracking_reference=provider_result.tracking_number,
            shipment_amount=provider_result.amount,
            label_url=provider_result.label_url
        )

        uow.order.save(order)
        uow.commit() # Saves the Tracking Ref and Label URL to DynamoDB

        return dtos.ResponseDTO(
            success=True,
            message=f"Fulfillment data attached for Shipment {data.shipment_id}."
        )

