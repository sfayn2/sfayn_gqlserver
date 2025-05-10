from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events, repositories

def handle_logged_order(
        event: events.OrderCancelled, 
        uow: repositories.UnitOfWorkAbstract, 
        logging_service: ports.LoggingServiceAbstract):

    logging_service.log(f"Order has been canceled {event.order_id}")
