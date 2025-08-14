from __future__ import annotations
import redis, os
from typing import Dict, List, Type
from ddd.order_management.domain import events, repositories
from ddd.order_management.application import dtos
from ddd.order_management.infrastructure import redis_services

#TODO should be here or bootstrap?
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(filename=".env.test"))

#NOTE: make sure bootstrap.py is called upfront to register event handlers(ex. apps.py? )
EVENT_HANDLERS: Dict[str, List] = {}
ASYNC_INTERNAL_EVENT_HANDLERS: Dict[str, List] = {}
ASYNC_EXTERNAL_EVENT_HANDLERS: Dict[str, List] = {}

# central mapping of event stream payloads to dtos.IntegrationEvent
EVENT_MODELS = Dict[str, Type[dtos.IntegrationEvent]]


# Config
REDIS_INTERNAL_URL = os.getenv("REDIS_INTERNAL_URL")
REDIS_INTERNAL_STREAM = os.getenv("REDIS_INTERNAL_STREAM")
REDIS_EXTERNAL_URL = os.getenv("REDIS_EXTERNAL_URL")
REDIS_EXTERNAL_STREAM = os.getenv("REDIS_EXTERNAL_STREAM")

EXTERNAL_EVENT_WHITELIST = set(
    e.strip() for e in os.getenv("EXTERNAL_EVENT_WHITELIST", "").split(",") if e.strip()
)

INTERNAL_EVENT_WHITELIST = set(
    e.strip() for e in os.getenv("INTERNAL_EVENT_WHITELIST", "").split(",") if e.strip()
)

_internal_publisher = None
_external_publisher = None

def get_internal_publisher() -> redis_services.RedisStreamPublisher:
    # keep connection alive and reuse
    global _internal_publisher

    if _internal_publisher is None:
        if not REDIS_INTERNAL_URL and REDIS_INTERNAL_STREAM:
            raise RuntimeError("Internal Redis config is missing")
        _internal_publisher = redis_services.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(REDIS_INTERNAL_URL, decode_responses=True),
            stream_name=REDIS_INTERNAL_STREAM
        )
    return _internal_publisher

def get_external_publisher() -> redis_services.RedisStreamPublisher:
    # keep connection alive and reuse
    global _external_publisher

    if _external_publisher is None:
        if not REDIS_EXTERNAL_URL and REDIS_EXTERNAL_STREAM:
            raise RuntimeError("External Redis config is missing")
        _external_publisher = redis_services.RedisStreamPublisher(
            redis_client=redis.Redis.from_url(REDIS_EXTERNAL_URL, decode_responses=True),
            stream_name=REDIS_EXTERNAL_STREAM
        )
    return _external_publisher




def publish(event: events.DomainEvent, uow: UnitOfWorkAbstract, **dependencies):
    # handle the synchronous event locally by triggering event handlers
    handlers = EVENT_HANDLERS.get(event, [])
    for handler in handlers:
        handler(event, uow, **dependencies)

    # internal event publisher raised by domain event
    if event.internal_event_type() in INTERNAL_EVENT_WHITELIST:
        try:
            get_internal_publisher().publish({
                "event_type": event.internal_event_type(),
                **event.to_dict()
            })
        except Exception as e:
            print(f"Failed to publish internal event {event.internal_event_type()}")

    # external event publisher raised by domain event
    if event.external_event_type() in EXTERNAL_EVENT_WHITELIST:
        try:
            get_external_publisher().publish({
                "event_type": event.external_event_type(),
                **event.to_dict()
            })
        except Exception as e:
            print(f"Failed to publish external event {event.external_event_type()}")

