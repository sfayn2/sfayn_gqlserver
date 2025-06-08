from __future__ import annotations
import json
import redis

#TODO make use of redis stream if we really want to evolve to full microservice?
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