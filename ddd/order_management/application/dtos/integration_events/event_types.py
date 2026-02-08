from enum import StrEnum

class IntegrationEventType(StrEnum):
    SHIPPING_TRACKER_WEBHOOK_RECEIVED = "shipping_tracker_webhook.received"
    ADD_ORDER_WEBHOOK_RECEIVED = "add_order_webhook.received"