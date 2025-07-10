from django.core.management.base  import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from ddd.order_management.infrastructure.redis_services import redis_stream_listener

        rsl = redis_stream_listener.RedisStreamListener(
            consumer_name="order_worker1",
            stream_name="stream.auth_service"
            )

        rsl.listen()
