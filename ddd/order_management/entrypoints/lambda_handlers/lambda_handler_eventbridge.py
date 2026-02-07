import json

BOOTSTRAPPED = False


def handler(event, context):
    global BOOTSTRAPPED
    if not BOOTSTRAPPED:
        from ddd.order_management.infrastructure import event_bus
        from ddd.order_management.bootstrap import bootstrap_aws
        bootstrap_aws.bootstrap_aws()
        BOOTSTRAPPED = True
    # AWS EventBridge top-level metadata
    event_type = event.get("detail-type")
    # 'detail' in EventBridge is already a dict if sent from boto3/PutEvents
    payload = event.get("detail", {})

    # 1. Look for handlers in BOTH registries
    internal_handlers = event_bus.ASYNC_INTERNAL_EVENT_HANDLERS.get(event_type, [])
    external_handlers = event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS.get(event_type, [])

    all_handlers = internal_handlers + external_handlers

    if all_handlers:
        for event_handler in all_handlers:
            # If payload was serialized as a string (common for legacy/external), parse it
            if isinstance(payload, str):
                payload = json.loads(payload)
            print(f"[Lambda EventBridge Handler] Processing event type: {event_type} with payload: {payload}")
                
            event_handler(payload)
    else:
        print(f"[Warning] No handler registered for event type: {event_type}")
