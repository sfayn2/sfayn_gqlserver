from __future__ import annotations
import redis
from typing import Dict, List
from ddd.order_management.domain import events, repositories
from ddd.order_management.infrastructure import redis_services

#Note: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}


def publish(event: events.DomainEvent, uow: UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event.event_type(), [])
    for handler in handlers:
        handler(event, uow, **dependencies)

    # TODO is this the correct place?
    # external async event publisher
    external_event_publisher = redis_services.RedisStreamPublisher(
        redis_client=redis.Redis.from_url(os.getenv("REDIS_EXTERNAL_URL"), decode_responses=True),
        stream_name=os.getenv("REDIS_EXTERNAL_STREAM")
    )

    external_event_publisher.publish({
        "event_type": event.event_type(),
        **event.to_dict()
    })

