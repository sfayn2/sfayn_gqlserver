from __future__ import annotations
import json
import redis

redis_client = redis.Redis.from_url('redis://localhost:6379')

claims = {
    "sub": "abc123",
    "email": "abc@email.com",
    "tenant_id": "tenant-abc",
    "realm_access": {
        "roles": ["customer"]
    },
    "vendor_id": "v-124",
    "vendor_name": "vendor 1",
    "vendor_country": "India",
    "shipping_address": {
        "street": "123 Main st",
        "city": "Metro city",
        "state": "Stat1",
        "postal": 1234,
        "country": "IX"
    }
}

event = {
    "event_type": "auth_service.events.UserLoggedInEvent",
    "user_id": "abc123",
    "claims": json.dumps(claims)
}

redis_client.xadd("stream.auth_service", event)