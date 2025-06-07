import json
import redis

redis_client = redis.Redis.from_url('redis://localhost:6379', decode_responses=True)

def redis_event_publish(self, event: events.DomainEvent, uow: repositories.UnitOfWorkAbstract):

    event_dict = {
        "event_type": event.event_type(),
        "payload": event.to_dict()
    }

    channel = event.event_type()

    redis_client.publish(
        channel, 
        json.dumps(event_dict)
    )