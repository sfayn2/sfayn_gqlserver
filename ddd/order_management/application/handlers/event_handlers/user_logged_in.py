from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events

#Async handler
def handle_user_logged_in(
    event
):

    #TODO do the snapshot here
    print(f"User has been logged in {event}")
