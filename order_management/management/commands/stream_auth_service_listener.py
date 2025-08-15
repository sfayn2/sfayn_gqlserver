import redis, os
from django.core.management.base  import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from ddd.order_management.infrastructure import (
            event_payload_decoders,
            event_listeners,
            event_bus
        )

        REDIS_CLIENT = redis.Redis.from_url(os.getenv("REDIS_IDP_URL"), decode_responses=True)

        rsl = event_listeners.RedisStreamListener(
            redis_client=REDIS_CLIENT,
            consumer_name="order_worker1",
            stream_name="stream.external.identity_gateway_service",
            event_handlers=event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS,
            event_payload_decoder=event_payload_decoders.RedisEventPayloadDecoder(event_bus.EVENT_MODELS)
            )

        rsl.listen()
