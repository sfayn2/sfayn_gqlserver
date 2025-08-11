from __future__ import annotations
import json
import redis

redis_client = redis.Redis.from_url('redis://localhost:6379')

#claims = {
#    "roles": ["customer"],
#    "email": "abc@email.com",
#    "given_name": "Given name1",
#    "family_name" : "family1",
#    "vendor_id": "v-124",
#    "vendor_name": "vendor 1",
#    "vendor_country": "India",
#    "shipping_address": {
#        "street": "123 Main st",
#        "city": "Metro city",
#        "state": "Stat1",
#        "postal": 1234,
#        "country": "IX"
#    }
#}

#event = {
#    "event_type": "auth_service.events.UserLoggedInEvent",
#    "sub": "abc123",
#    "token_type": "Bearer",
#    "tenant_id": "t-123",
#    "claims": json.dumps(claims)
#}

event = {
    "event_type": "identity_gateway_service.external_events.UserLoggedInEvent",
    "sub": "abc123",
    "token_type": "Bearer",
    "tenant_id": "t-123",
    "roles": json.dumps(["customer"])
}

redis_client.xadd("stream.identity_gateway_service", event)