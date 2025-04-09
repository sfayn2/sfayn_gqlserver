from typing import Union
from ddd.order_management.domain import events
from ddd.order_management.application import ports, handlers
from ddd.order_management.infrastructure.adapters import (
    email_service, 
    logging_service
)


EVENT_HANDLERS = {
    events.OrderCancelled: [
        lambda event, uow: handlers.handle_logged_order(event, uow, logging_service=logging_service.LoggingService()),
        lambda event, uow: handlers.handle_email_canceled_order(event, uow, email_service=email_service.EmailService())
        ]
}

def publish(event: events.DomainEvent, uow: ports.UnitOfWorkAbstract):
    # handle the event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(type(event), [])
    for handler in handlers:
        handler(event, uow)

    # TODO?
    # publish the event  using the event publisher (Redis, Kafka, RabbitMQ, etc.?)