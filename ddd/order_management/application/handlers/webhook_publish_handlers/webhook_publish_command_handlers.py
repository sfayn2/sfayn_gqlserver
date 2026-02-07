

def get_command_handlers(commands, handlers, event_bus, shipping_webhook_parser, webhook_receiver_service, shipment_lookup_service, tracking_reference_extractor):
    return {
        commands.PublishAddOrderCommand: lambda command, **deps: handlers.handle_publish_add_order(
            command=command,
            event_publisher=event_bus.internal_publisher,
            webhook_receiver_service=webhook_receiver_service,
            **deps
        ),
        commands.PublishShipmentTrackerCommand: lambda command, **deps: handlers.handle_publish_shipment_tracker(
            command=command,
            event_publisher=event_bus.internal_publisher,
            webhook_receiver_service=webhook_receiver_service,
            shipment_lookup_service=shipment_lookup_service,
            shipping_webhook_parser=shipping_webhook_parser,
            tracking_reference_extractor=tracking_reference_extractor,
            **deps
        ),
    }
