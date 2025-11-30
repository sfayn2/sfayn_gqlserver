from __future__ import annotations
from ddd.order_management.application import dtos

class ConfigMapper:

    @staticmethod
    def to_create_shipment_config_dto(config_source: dict) -> dtos.CreateShipmentConfigDTO:
        provider_value = config_source.get("shipment")
        apikey_value = config_source.get("apikey")
        endpoint_value = config_source.get("endpoint")
    
        if provider_value is None:
            raise ValueError("Create Shipment Api provider must be specified in the configuration.")
        if apikey_value is None:
            raise ValueError("Create Shipment Api key must be specified in the configuration.")
        if endpoint_value is None:
            raise ValueError("Create Shipment endpoint must be specified in the configuration.")

        # Map specific keys for the shipment tracker
        return dtos.CreateShipmentConfigDTO(
            # Assumes the keys in the DB are 'shipment_shared_secret' and 'shipment_max_age'
            provider=provider_value,
            api_key=apikey_value,
            endpoint=endpoint_value
        )

    @staticmethod
    def to_shipment_tracker_config_dto(config_source: dict) -> dtos.WebhookReceiverConfigDTO:
        shipment_tracker_config = config_source.get("shipment_tracker", {})
        if not shipment_tracker_config:
            raise Exception("Missing shipment_tracker config for this tenant.")

        provider_value = shipment_tracker_config.get("provider")
        shared_secret_value = shipment_tracker_config.get("shared_secret")
        max_age_seconds_value = shipment_tracker_config.get("max_age_seconds")
    
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
    def to_add_order_config_dto(config_source: dict) -> dtos.WebhookReceiverConfigDTO:
        add_order_config = config_source.get("add_order", {})
        if not add_order_config:
            raise Exception("Missing add_order config for this tenant.")

        provider_value = add_order_config.get("provider")
        shared_secret_value = add_order_config.get("shared_secret")
        max_age_seconds_value = add_order_config.get("max_age_seconds")
    
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