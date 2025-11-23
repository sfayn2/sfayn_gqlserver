from __future__ import annotations
from typing import Any
from ddd.order_management.application import dtos
# Consider using a standard library for time parsing like iso8601 or datetime
from datetime import datetime


# Inheriting from an abstract base class (ABC) is good practice for handlers
# class ShippingWebhookPayloadHandlerAbstract: ...

class EasyPostShippingWebhookPayloadHandler:
    """
    Handles parsing EasyPost webhook payloads into a standardized DTO.
    """

    def parse(self, payload: dict[str, Any], headers: dict[str, Any]) -> dtos.ShippingWebhookIntegrationEvent:
        """
        Parses the raw webhook payload dictionary into a structured integration event DTO.

        Args:
            payload: The raw dictionary received from the webhook body.
            headers: The raw dictionary of HTTP headers (unused here, but useful for validation).

        Returns:
            A ShippingWebhookIntegrationEvent instance.

        Raises:
            KeyError: If essential keys are missing from the payload structure.
            ValueError: If data types are incorrect (e.g., date format).
        """
        try:
            # 1. Type Hinting: Use explicit dict[str, Any] for clarity.
            # 2. Defensive Access: Use .get() where possible or wrap in try/except for mandatory keys.

            tracking_reference = payload["result"]["tracking_code"]
            tenant_id = payload["metadata"]["tenant_id"]
            status = payload["description"]
            occurred_at_str = payload["created_at"]

            # 3. Data Transformation: Convert the string timestamp into a proper datetime object
            # if your DTO expects one (highly recommended).
            # Example format: '2023-10-27T12:00:00Z'
            occurred_at = datetime.fromisoformat(occurred_at_str)

            # 4. Use intermediate variables for clarity before instantiation.
            payload_dto = dtos.ShippingWebhookPayloadDTO(
                provider="easypost",
                tracking_reference=tracking_reference,
                tenant_id=tenant_id,
                status=status,
                occured_at=occurred_at,
                raw_payload=payload
            )

            return dtos.ShippingWebhookIntegrationEvent(
                event_type="webhook_events.ShippingTracker",
                data=payload_dto,
            )

        except KeyError as e:
            # Handle missing mandatory fields gracefully
            raise Exception(f"Missing required key in EasyPost payload: {e}") from e
        except (TypeError, ValueError) as e:
            # Handle invalid data types or formats (e.g., bad date string)
            raise Exception(f"Invalid data format in EasyPost payload: {e}") from e

