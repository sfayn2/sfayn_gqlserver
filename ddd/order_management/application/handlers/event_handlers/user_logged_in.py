from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

#Async handler
def handle_user_logged_in(
    event: dtos.UserLoggedInIntegrationEvent,
    auth_sync: ports.SnapshotSyncServiceAbstract
):

    try:
        event_payloads = dtos.UserLoggedInIntegrationEvent(**event)
    except Exception as e:
        raise exceptions.IntegrationException(f"Invalid event payload {e}")

    auth_sync.sync(event_payloads)
    if "customer" in event_payloads.roles:
        customer_sync.sync(event_payloads)
    #if "vendor" in event_payloads.roles:
    #    vendor_sync.sync(event_payloads)


    print(f"User has been logged in {event_payloads}")
