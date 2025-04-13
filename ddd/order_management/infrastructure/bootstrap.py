
from typing import Union
from ddd.order_management.domain import events
from ddd.order_management.application import handlers
from ddd.order_management.infrastructure import event_bus
from ddd.order_management.infrastructure.adapters import (
    email_service, 
    logging_service
)

#Depending on the framework arch this might be inside manage.py , app.py, or main.py ?
def register_event_handlers():
    event_bus.EVENT_HANDLERS.update({
        events.OrderCancelled: [
            lambda event, uow: handlers.handle_logged_order(event, uow, logging_service=logging_service.LoggingService()),
            lambda event, uow: handlers.handle_email_canceled_order(event, uow, email_service=email_service.EmailService())
            ]
    })