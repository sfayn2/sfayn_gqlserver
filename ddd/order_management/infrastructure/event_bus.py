from __future__ import annotations
import redis, os
from typing import Dict, List, Type, Any, Optional
from ddd.order_management.domain import events, repositories
from ddd.order_management.application import dtos, ports

#NOTE: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[Type[events.DomainEvent], List[Any]] = {}
ASYNC_INTERNAL_EVENT_HANDLERS: Dict[str, List[Any]] = {}
ASYNC_EXTERNAL_EVENT_HANDLERS: Dict[str, List[Any]] = {}

# central mapping of event stream payloads to dtos.IntegrationEvent
EVENT_MODELS: Dict[str, Type[dtos.IntegrationEvent]] = {}

EXTERNAL_EVENT_WHITELIST: List[str] = []
INTERNAL_EVENT_WHITELIST: List[str] = []

internal_publisher: Optional[ports.EventPublisherAbstract] = None 
external_publisher: Optional[ports.EventPublisherAbstract] = None


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


def publish(event: events.DomainEvent, uow: ports.UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(type(event), [])
    for handler in handlers:
        handler(event, uow, **dependencies)
    
    publish_async_internal(event)
    publish_async_external(event)



