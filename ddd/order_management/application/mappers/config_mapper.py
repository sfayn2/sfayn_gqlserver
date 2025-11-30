from __future__ import annotations
from ddd.order_management.application import dtos

class ConfigMapper:

    @staticmethod
    def to_shipment_config_dto(config_source: dict) -> dtos.ShipmentWebhookConfigDTO:
        provider_value = config_source.get("shipment_provider")
        apikey_value = config_source.get("apikey_provider")
        endpoint_value = config_source.get("endpoint_provider")
    
        if provider_value is None:
            raise ValueError("Shipment webhook provider must be specified in the configuration.")
        if apikey_value is None:
            raise ValueError("Shipment webhook api key must be specified in the configuration.")
        if endpoint_value is None:
            raise ValueError("Shipment webhook endpoint must be specified in the configuration.")

        # Map specific keys for the shipment tracker
        return dtos.ShipmentWebhookConfigDTO(
            # Assumes the keys in the DB are 'shipment_shared_secret' and 'shipment_max_age'
            provider=provider_value,
            api_key=apikey_value,
            endpoint=endpoint_value
        )

    @staticmethod
    def to_shipment_tracker_config_dto(config_source: dict) -> dtos.WebhookReceiverConfigDTO:
        provider_value = config_source.get("shipment_provider")
        shared_secret_value = config_source.get("shipment_webhook_shared_secret")
        max_age_seconds_value = config_source.get("shipment_webhook_max_age_seconds")
    
        if provider_value is None:
            raise ValueError("Shipment tracker webhook provider must be specified in the configuration.")

        if shared_secret_value is None:
            raise ValueError("Shipment tracker webhook shared secret must be specified in the configuration.")

        if max_age_seconds_value is None:
            raise ValueError("Shipment tracker webhook max age seconds must be specified in the configuration.")

        # Map specific keys for the shipment tracker
        return dtos.WebhookReceiverConfigDTO(
            # Assumes the keys in the DB are 'shipment_shared_secret' and 'shipment_max_age'
            provider=provider_value,
            shared_secret=shared_secret_value,
            max_age_seconds=max_age_seconds_value
        )

    @staticmethod
    def to_order_config_dto(config_source: dict) -> dtos.WebhookReceiverConfigDTO:
        provider_value = config_source.get("shipment_provider")
        shared_secret_value = config_source.get("shipment_webhook_shared_secret")
        max_age_seconds_value = config_source.get("shipment_webhook_max_age_seconds")
    
        if provider_value is None:
            raise ValueError("Add Order webhook provider must be specified in the configuration.")

        if shared_secret_value is None:
            raise ValueError("Add Order webhook shared secret must be specified in the configuration.")

        if max_age_seconds_value is None:
            raise ValueError("Add Order webhook max age seconds must be specified in the configuration.")

        # Map specific keys for the add order webhook
        return dtos.WebhookReceiverConfigDTO(
            provider=provider_value,
            shared_secret=shared_secret_value,
            max_age_seconds=max_age_seconds_value
        )