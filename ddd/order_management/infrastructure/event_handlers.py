from ddd.order_management.domain import events
from ddd.order_management.infrastructure import unit_of_work, email_service, logging_service

def handle_logged_order(
        event: events.OrderCancelled, 
        uow: unit_of_work.DjangoOrderUnitOfWork, 
        logging_service: logging_service.LoggingService):

    logging_service.log(f"Order has been canceled {event.order_id}")

def handle_email_canceled_order(
        event: events.OrderCancelled, 
        uow: unit_of_work.DjangoOrderUnitOfWork, 
        email_service: email_service.EmailService):

    msg = f"Order has been canceled {event.order_id}"
    email_service.send_email(msg)