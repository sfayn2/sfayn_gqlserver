from __future__ import annotations
from ddd.order_management.application import dtos

class ConfigMapper:

    @staticmethod
    def to_shipment_config_dto(config_source: dict) -> dtos.ShipmentWebhookConfigDTO:
        shipment_config = dtos.ShipmentWebhookConfigDTO(
            shipment_provider=config_source["shipment_provider"],
            shipment_api_key=config_source["shipment_api_key"],
            shipment_endpoint=config_source["shipment_endpoint"],
            shipment_webhook_shared_secret=config_source["shipment_webhook_shared_secret"],
            shipment_webhook_max_age_seconds=config_source["shipment_webhook_max_age_seconds"],
        )
        return shipment_config