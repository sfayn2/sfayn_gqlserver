import redis, os
from django.core.management.base  import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from ddd.order_management.infrastructure.redis_services import redis_stream_listener
        from ddd.order_management.infrastructure.event_bus import ASYNC_EXTERNAL_EVENT_HANDLERS

        REDIS_CLIENT = redis.Redis.from_url(os.getenv("REDIS_IDP_URL"), decode_responses=True)

        rsl = redis_stream_listener.RedisStreamListener(
            redis_client=REDIS_CLIENT,
            consumer_name="order_worker1",
            stream_name="stream.external.identity_gateway_service",
            event_handlers=ASYNC_EXTERNAL_EVENT_HANDLERS
            )

        rsl.listen()
