from typing import Dict, List
from ddd.order_management.domain import events, repositories
from ddd.order_management.infrastructure.redis_event_publisher import redis_event_publish

#TODO: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}

def publish(event: events.DomainEvent, **dependencies):
    # handle the event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event.event_type, [])
    for handler in handlers:
        handler(event, **dependencies)

    # TODO publish async event for external handler?
    #redis_event_publish(event=event, uow=uow)
