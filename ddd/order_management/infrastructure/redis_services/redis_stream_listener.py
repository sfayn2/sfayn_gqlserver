import redis
import json
from typing import List, Dict
from ddd.order_management.application import ports
#from ddd.order_management.infrastructure.event_bus import ASYNC_EVENT_HANDLERS

# =================
# To Consume Auth Service Logged In user
# =================
#redis_client = redis.Redis.from_url('redis://localhost:6379', decode_responses=True)
#group_name = "order_management_service"
#consumer_name = "order_worker1"
#stream_name = "stream.auth_service"


# ===========
# To consumer any stream service 

class RedisStreamListener(ports.EventListenerAbstract):
    def __init__(self, redis_client: redis.Redis, stream_name: str, consumer_name: str, group_name: str = "order_management_service", event_handlers: Dict[str, List] = {}):
        #self.redis_client = redis.Redis.from_url('redis://localhost:6379', decode_responses=True)
        self.redis_client = redis_client
        self.group_name = group_name
        self.consumer_name = consumer_name
        self.stream_name = stream_name
        self.event_handlers = event_handlers
        self._ensure_group()

    def _ensure_group(self):
        try:
            self.redis_client.xgroup_create(self.stream_name, self.group_name, id="0", mkstream=True)
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    def listen(self):
        print(f"Start Redis Stream listener for {self.stream_name}")
        while True:

            # read all unack first
            messages = self.redis_client.xreadgroup(self.group_name, self.consumer_name, {self.stream_name: "0"}, count=10)

            # if no pending msgs, read new
            if messages == [[self.stream_name, []]]:
                messages = self.redis_client.xreadgroup(self.group_name, self.consumer_name, {self.stream_name: ">"}, count=10, block=5000)

            for stream, events in messages:
                for msg_id, event in events:
                    event_type = event.get("event_type")

                    #handlers = ASYNC_EVENT_HANDLERS.get(event_type, [])
                    handlers = event_handlers.get(event_type, [])
                    if handlers:
                        for handler in handlers:
                            event["roles"] = json.loads(event["roles"])
                            handler(event)
                        self.redis_client.xack(self.stream_name, self.group_name, msg_id)
                    else:
                        print(f"Unknown event type {event_type}")


