from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_product_update_async_event(
    event: dtos.ProductUpdateIntegrationEvent,
    product_sync: ports.SnapshotSyncServiceAbstract
):

    try:
        event1 = {
            "event_type": event.get("event_type"),
            "data": json.loads(event.get("data"))
        }
        event_payloads = dtos.ProductUpdateIntegrationEvent(**event1)
    except Exception as e:
        raise exceptions.IntegrationException(f"Invalid event payload {e}")

    # sync external produc snapshot sync
    product_sync.sync(event_payloads)

    print(f"Product has been updated {event_payloads}")
