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

    # Identify which bus triggered this lambda
    # Example ARN: arn:aws:events:us-east-1:123456789012:event-bus/default_external
    bus_resources = event.get("resources", [])
    triggering_bus_arn = bus_resources[0] if bus_resources else ""
    
    is_external = "default_external" in triggering_bus_arn
    
    if is_external:
        # Use the shared registry from your infrastructure layer
        event_handlers_registry = event_bus.ASYNC_EXTERNAL_EVENT_HANDLERS
    else:
        event_handlers_registry = event_bus.ASYNC_INTERNAL_EVENT_HANDLERS

    handlers = event_handlers_registry.get(event_type, [])

    if handlers:
        for event_handler in handlers:
            # If payload was serialized as a string (common for legacy/external), parse it
            if isinstance(payload, str):
                payload = json.loads(payload)
                
            event_handler(payload)
    else:
        print(f"[Warning] No handler registered for event type: {event_type}")
