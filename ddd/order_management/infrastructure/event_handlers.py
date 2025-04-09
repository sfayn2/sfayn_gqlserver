from ddd.order_management.domain import events
from ddd.order_management.application import ports

def handle_logged_order(
        event: events.OrderCancelled, 
        uow: ports.UnitOfWorkAbstract, 
        logging_service: ports.LoggingServiceAbstract):

    logging_service.log(f"Order has been canceled {event.order_id}")

def handle_email_canceled_order(
        event: events.OrderCancelled, 
        uow: ports.UnitOfWorkAbstract, 
        email_service: ports.EmailServiceAbstract):

    msg = f"Order has been canceled {event.order_id}"
    email_service.send_email(msg)