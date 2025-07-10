from __future__ import annotations
import json
import redis

redis_client = redis.Redis.from_url('redis://localhost:6379')

claims = {
    "sub": "abc123",
    "email": "abc@email.com"
}

event = {
    "event_type": "auth_service.events.UserLoggedInEvent",
    "user_id": 1,
    "claims": json.dumps(claims)
}

redis_client.xadd("stream.auth_service", event)