import os
import redis
import logging
from ddd.order_management.infrastructure.bootstrap import bootstrap_onprem

# 1. Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_worker():
    """
    Standalone entrypoint to consume Redis Streams.
    Replaces the Django management command.
    """
    logger.info("Starting Redis Stream Worker (Internal)...")


    from ddd.order_management.infrastructure import (
        event_payload_decoders,
        event_listeners
    )

    # 3. Setup Redis Connection
    REDIS_CLIENT = redis.Redis.from_url(
        os.getenv("REDIS_INTERNAL_URL"), 
        decode_responses=True
    )

    # 4. Initialize the Listener
    rsl = event_listeners.RedisStreamListener(
        redis_client=REDIS_CLIENT,
        consumer_name=os.getenv("REDIS_CONSUMER_NAME", "order_internal_worker"),
        stream_name=os.getenv("REDIS_INTERNAL_STREAM"),
        event_handlers=event_bus.ASYNC_INTERNAL_EVENT_HANDLERS,
        event_payload_decoder=event_payload_decoders.RedisEventPayloadDecoder(
            event_bus.EVENT_MODELS
        )
    )

    # 5. Start Listening (Blocking Loop)
    try:
        rsl.listen()
    except KeyboardInterrupt:
        logger.info("Worker stopped by user.")
    except Exception as e:
        logger.error(f"Worker crashed: {e}")

if __name__ == "__main__":
    # Ensure Django environment is loaded if using Django models in handlers
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    
    run_worker()

