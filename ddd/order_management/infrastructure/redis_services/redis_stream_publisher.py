import json
import redis

from ddd.order_management.application import ports

class RedisStreamPublisher(ports.EventPublisherAbstract):
    def __init__(self, redis_client: redis.Redis, stream_name: str):
        #self.redis_client = redis.Redis.from_url('redis://localhost:6379', decode_responses=True)
        self.redis_client = redis_client
        self.stream_name = stream_name

    def publish(self, event):
        self.client.xadd(self.stream_name, event)