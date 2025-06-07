import json
import asyncio
import redis.asyncio as aioredis
from ddd.order_management.infrastructure.event_bus import EVENT_HANDLERS

#TODO make use of redis stream if we really want to evolve to full microservice?
redis_client = aioredis.from_url('redis://localhost:6379', decode_responses=True)

async def redis_event_subscribe(event_types: list[str]):
    pubsub = redis_client.pubsub()
    channels = [et for et in event_types]
    await pubsub.subscribe(*channels)

    print(f"Subscribed to channels: {channels}")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            event_data = json.loads(message["data"])
            event_type = event_data["event_type"]
            payload = event_data["payload"]

            print(f"[RedisConsumer] Received event: {event_type}")

            handlers = EVENT_HANDLERS.get(event_type, [])
            await asyncio.gather(*(handler(payload, uow) for handler in handlers))

        except Exception as e:
            print(f"[RedisConsumer] Error handling event: {e}")

async def main():
    await redis_event_subscribe([
        "vendor_management.events.VendorOffersCreateEvent"
    ])

if __name__ == "__main__":
    asyncio.run(main())
