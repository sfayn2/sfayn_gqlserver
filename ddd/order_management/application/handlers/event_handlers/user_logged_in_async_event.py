from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

# type: ignore

#Async handler
def handle_user_logged_in_async_event(
    event: dtos.UserLoggedInIntegrationEvent,
):

    #try:
    #    event_payloads = dtos.UserLoggedInIntegrationEvent(**event)
    #except Exception as e:
    #    raise exceptions.IntegrationException(f"Invalid event payload {e}")

    #auth_snapshot_repo.sync(event_payloads)
    #if "customer" in event_payloads.roles:
    #    customer_snapshot_repo.sync(event_payloads)


    print(f"User has been logged in {event}")
