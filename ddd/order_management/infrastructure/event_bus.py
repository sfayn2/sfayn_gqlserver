from __future__ import annotations
import redis, os
from typing import Dict, List, Type
from ddd.order_management.domain import events, repositories
from ddd.order_management.application import dtos

#NOTE: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}
ASYNC_INTERNAL_EVENT_HANDLERS: Dict[str, List] = {}
ASYNC_EXTERNAL_EVENT_HANDLERS: Dict[str, List] = {}

# central mapping of event stream payloads to dtos.IntegrationEvent
EVENT_MODELS = Dict[str, Type[dtos.IntegrationEvent]]

EXTERNAL_EVENT_WHITELIST = []
INTERNAL_EVENT_WHITELIST = []
internal_publisher = None
external_publisher = None


def publish_async_internal(event: events.DomainEvent):
    # internal event publisher raised by domain event
    if event.internal_event_type() in INTERNAL_EVENT_WHITELIST:

        if internal_publisher is None:
            raise RuntimeError("Internal Publisher config is missing")

        try:
            internal_publisher.publish({
                "event_type": event.internal_event_type(),
                **event.to_dict()
            })
        except Exception as e:
            print(f"Failed to publish internal event {event.internal_event_type()}")

def publish_async_external(event: events.DomainEvent):
    # external event publisher raised by domain event
    if event.external_event_type() in EXTERNAL_EVENT_WHITELIST:

        if external_publisher is None:
            raise RuntimeError("External Publisher config is missing")

        try:
            external_publisher.publish({
                "event_type": event.external_event_type(),
                **event.to_dict()
            })
        except Exception as e:
            print(f"Failed to publish external event {event.external_event_type()}")


def publish(event: events.DomainEvent, uow: UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event, [])
    for handler in handlers:
        handler(event, uow, **dependencies)
    
    publish_async_internal(event)
    publish_async_external(event)



