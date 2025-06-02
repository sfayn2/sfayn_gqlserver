from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events

def handle_email_canceled_order(
        event: events.OrderCancelled, 
        uow: UnitOfWorkAbstract, 
        email: EmailAbstract):

    msg = f"Order has been canceled {event.order_id}"
    email.send_email(msg)
