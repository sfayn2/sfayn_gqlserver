from typing import Dict, List
from ddd.order_management.application import ports
from ddd.order_management.domain import events

#TODO: make sure bootstrap.py is called upfront to register event handlers(ex. manage.py ? or apps.py? )
EVENT_HANDLERS: Dict[events.DomainEvent, List] = {}

def publish(event: events.DomainEvent, uow: ports.UnitOfWorkAbstract):
    # handle the event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(type(event), [])
    for handler in handlers:
        handler(event, uow)

    # TODO?
    # publish the event  using the event publisher (Redis, Kafka, RabbitMQ, etc.?)