import json
import redis
from typing import List
from decimal import Decimal

from ddd.order_management.application import ports

class RedisStreamPublisher(ports.EventPublisherAbstract):
    def __init__(self, redis_client: redis.Redis, stream_name: str, event_whitelist: List[str]):
        #self.redis_client = redis.Redis.from_url('redis://localhost:6379')
        self.redis_client = redis_client
        self.stream_name = stream_name
        self.event_white_list = event_whitelist

    def publish(self, event):
        try:
            if event.event_type in self.event_white_list:
                final_payload = {
                    "event_type": event.event_type,
                    "data": event.data.model_dump_json()
                }
                self.redis_client.xadd(self.stream_name, final_payload)
            else:
                print(f"[RedisStreamPublisher] Not allowed publish event for {event.event_type}")
        except Exception as e:
            #log?
            print(f"[RedisStreamPublisher] {e}")
