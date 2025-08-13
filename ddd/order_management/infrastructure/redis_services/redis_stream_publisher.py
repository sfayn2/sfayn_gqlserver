import json
import redis
from decimal import Decimal

from ddd.order_management.application import ports

class RedisStreamPublisher(ports.EventPublisherAbstract):
    def __init__(self, redis_client: redis.Redis, stream_name: str):
        #self.redis_client = redis.Redis.from_url('redis://localhost:6379')
        self.redis_client = redis_client
        self.stream_name = stream_name

    def publish(self, event):
        try:
            final_payload = {
                "event_type": event.event_type,
                "data": event.data.model_dump_json()
            }
            self.redis_client.xadd(self.stream_name, final_payload)
        except Exception as e:
            #log?
            print(f"[RedisStreamPublisher] {e}")
