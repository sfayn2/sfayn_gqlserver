from __future__ import annotations
from ddd.order_management.application import dtos

class ConfigMapper:

    @staticmethod
    def to_shipment_config_dto(config_source: dtos.TenantDTO) -> dtos.ShipmentWebhookConfigDTO:
        # Map specific keys for the shipment tracker
        return dtos.ShipmentWebhookConfigDTO(
            # Assumes the keys in the DB are 'shipment_shared_secret' and 'shipment_max_age'
            provider=config_source.configs.get("shipment_provider"),
            api_key=config_source.configs.get("shipment_api_key"),
            endpoint=config_source.configs.get("shipment_endpoint")
        )

    @staticmethod
    def to_shipment_tracker_config_dto(config_source: dtos.TenantDTO) -> dtos.WebhookReceiverConfigDTO:
        # Map specific keys for the shipment tracker
        return dtos.WebhookReceiverConfigDTO(
            # Assumes the keys in the DB are 'shipment_shared_secret' and 'shipment_max_age'
            provider=config_source.configs.get("shipment_provider"),
            shared_secret=config_source.configs.get("shipment_webhook_shared_secret"),
            max_age_seconds=config_source.configs.get("shipment_webhook_max_age_seconds")
        )

    @staticmethod
    def to_order_config_dto(config_source: dtos.TenantDTO) -> dtos.WebhookReceiverConfigDTO:
        # Map specific keys for the add order webhook
        return dtos.WebhookReceiverConfigDTO(
            provider=config_source.configs.get("add_order_webhook_provider"),
            shared_secret=config_source.configs.get("add_order_webhook_shared_secret"),
            max_age_seconds=config_source.configs.get("add_order_webhook_max_age_seconds")
        )