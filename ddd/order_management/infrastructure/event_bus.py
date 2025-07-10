from __future__ import annotations
from typing import Dict, List
from ddd.order_management.domain import events, repositories
from ddd.order_management.infrastructure import redis_services

#TODO: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}
ASYNC_EVENT_HANDLERS: Dict[str, List] = {}

def publish(event: events.DomainEvent, uow: UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event.event_type(), [])
    for handler in handlers:
        handler(event, uow, **dependencies)

    # TODO publish async event for external handler?
    #redis_event_publish(event=event, uow=uow)
    #redis_services.redis_stream_publisher.publish_event(event=event)
