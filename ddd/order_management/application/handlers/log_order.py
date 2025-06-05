from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events

def handle_logged_order(
        event: events.DomainEvent, 
        uow: repositories.UnitOfWorkAbstract, 
        logging: LoggingAbstract):

    logging.log(f"Order has been canceled {event.order_id}")
