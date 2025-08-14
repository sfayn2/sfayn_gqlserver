import redis, os
from django.core.management.base  import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from ddd.order_management.infrastructure.redis_services import redis_stream_listener
        from ddd.order_management.infrastructure import event_payload_decoders
        from ddd.order_management.infrastructure import event_bus

        REDIS_CLIENT = redis.Redis.from_url(os.getenv("REDIS_INTERNAL_URL"), decode_responses=True)

        rsl = redis_stream_listener.RedisStreamListener(
            redis_client=REDIS_CLIENT,
            consumer_name="order_internal_worker",
            stream_name=os.getenv("REDIS_INTERNAL_STREAM"),
            event_handlers=event_bus.ASYNC_INTERNAL_EVENT_HANDLERS,
            event_payload_decoder=event_payload_decoders.RedisEventPayloadDecoder(event_bus.EVENT_MODELS)
            )

        rsl.listen()
