

def get_command_handlers(commands, handlers, event_bus):
    return {
        commands.PublishProductUpdateCommand: lambda command, **deps: handlers.handle_publish_product_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorDetailsUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_details_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorCouponUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_coupon_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorOfferUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_offer_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorShippingOptionUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_shippingoption_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorPaymentOptionUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_paymentoption_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        ),
        commands.PublishVendorTaxOptionUpdateCommand: lambda command, **deps: handlers.handle_publish_vendor_taxoption_update(
            command=command,
            event_publisher=event_bus.internal_publisher,
            **deps
        )
    }
