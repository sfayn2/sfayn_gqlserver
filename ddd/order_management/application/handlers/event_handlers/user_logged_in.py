from __future__ import annotations
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

#Async handler
def handle_user_logged_in(
    event: dtos.UserLoggedInIntegrationEvent,
    auth_sync: ports.SnapshotSyncServiceAbstract,
    customer_sync: ports.SnapshotSyncServiceAbstract,
    vendor_sync: ports.SnapshotSyncServiceAbstract
):

    try:
        event_payloads = dtos.UserLoggedInIntegrationEvent(**event)
    except Exception as e:
        rasise exceptions.IntegrationException(f"Invalid event payload {e}")

    auth_sync.sync(event)
    if "customer" in event.claims.realm_access.roles:
        customer_sync.sync(event)
    if "vendor" in event.claims.realm_access.roles:
        vendor_sync.sync(event)


    print(f"User has been logged in {event}")
