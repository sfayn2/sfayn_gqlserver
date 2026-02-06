from __future__ import annotations
import json
from ddd.order_management.application import (
    mappers,
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions, models

def handle_shipment_tracker_async_event(
    event: dtos.ShippingWebhookIntegrationEvent,
    user_action_service: ports.UserActionServiceAbstract,
    uow: ports.UnitOfWorkAbstract):

    print("Processing shipment tracker async event:", event)