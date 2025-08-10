from __future__ import annotations
import redis, os
from typing import Dict, List
from ddd.order_management.domain import events, repositories
from ddd.order_management.infrastructure import redis_services

#Note: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}

external_event_publisher = redis_services.RedisStreamPublisher(
    redis_client=redis.Redis.from_url(os.getenv("REDIS_EXTERNAL_URL"), decode_responses=True),
    stream_name=os.getenv("REDIS_EXTERNAL_STREAM")
)

internal_event_publisher = redis_services.RedisStreamPublisher(
    redis_client=redis.Redis.from_url(os.getenv("REDIS_INTERNAL_URL"), decode_responses=True),
    stream_name=os.getenv("REDIS_INTERNAL_STREAM")
)

EXTERNAL_EVENT_WHITELIST = set(
    e.strip() for e in os.getenv("EXTERNAL_EVENT_WHITELIST", "").split(",") if strip()
)

INTERNAL_EVENT_WHITELIST = set(
    e.strip() for e in os.getenv("INTERNAL_EVENT_WHITELIST", "").split(",") if strip()
)


def publish(event: events.DomainEvent, uow: UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event.event_type(), [])
    for handler in handlers:
        handler(event, uow, **dependencies)

    # internal event publisher raised by domain event
    if event.event_type() in INTERNAL_EVENT_WHITELIST:
        internal_event_publisher.publish({
            "event_type": event.event_type(),
            **event.to_dict()
        })

    # external event publisher raised by domain event
    if event.event_type() in EXTERNAL_EVENT_WHITELIST:
        external_event_publisher.publish({
            "event_type": event.event_type(),
            **event.to_dict()
        })

