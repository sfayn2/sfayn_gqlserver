
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events, repositories

def handle_email_canceled_order(
        event: events.OrderCancelled, 
        uow: repositories.UnitOfWorkAbstract, 
        email_service: ports.EmailServiceAbstract):

    msg = f"Order has been canceled {event.order_id}"
    email_service.send_email(msg)
