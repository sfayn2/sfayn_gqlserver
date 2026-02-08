from __future__ import annotations
import json
from ddd.order_management.application import (
    mappers,
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions, models, enums

def handle_shipment_tracker_async_event(
    event: dtos.ShippingWebhookIntegrationEvent,
    user_action_service: ports.UserActionServiceAbstract,
    uow: ports.UnitOfWorkAbstract):

    print("Processing shipment tracker async event:", event)

    data = event.data
    
    with uow:
        order = uow.orders.get(data.order_id)
        if not order:
            return

        # 1. Map the incoming status to a Domain Action
        # This keeps the "Provider String" out of your Domain Models
        status_action = data.status.upper()

        try:
            # 2. Find the shipment ID first (since your methods use shipment_id)
            shipment = order.get_shipment_by_tracking(data.tracking_reference)
            sid = shipment.shipment_id

            # 3. Call the EXACT domain method for that intent
            if status_action == enums.ShipmentStatus.IN_TRANSIT.value:
                order.dispatch_shipment(sid, data.tracking_reference)
            elif status_action == enums.ShipmentStatus.DELIVERED.value:
                order.deliver_shipment(sid)
            elif status_action == enums.ShipmentStatus.CANCELLED.value:
                order.cancel_shipment(sid)
                # If your domain logic for 'shipped' is handled by dispatch:
                # order.dispatch_shipment(...)
                # Or if you just want to move the status:
            uow.commit()

        except exceptions.DomainError as e:
            print(f"Skipping update: {e}")
