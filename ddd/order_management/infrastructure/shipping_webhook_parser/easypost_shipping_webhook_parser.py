from __future__ import annotations
from typing import Any
from ddd.order_management.application import dtos
# Consider using a standard library for time parsing like iso8601 or datetime
from datetime import datetime


# Inheriting from an abstract base class (ABC) is good practice for handlers
# class ShippingWebhookPayloadHandlerAbstract: ...

class ShippingWebhookParserError(Exception):
    pass

class EasyPostShippingWebhookParser:
    """
    Handles parsing EasyPost webhook payloads into a standardized DTO.
    """

    def parse(self, payload: dict[str, Any]) -> dtos.ShippingWebhookRequestDTO:
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

            result = payload["result"]
            tracking_reference = result["tracking_code"]
            tenant_id = result["metadata"]["tenant_id"]
            order_id = result["metadata"]["order_id"]
            status = result["status"]
            occurred_at_str = payload.get("created_at") or payload.get("updated_at")

            # 3. Data Transformation: Convert the string timestamp into a proper datetime object
            # if your DTO expects one (highly recommended).
            # Example format: '2023-10-27T12:00:00Z'
            if occurred_at_str:
                occurred_at = datetime.fromisoformat(
                    occurred_at_str.replace("Z", "+00:00")
                )
            else:
                raise ShippingWebhookParserError("The 'occurred_at/updated_at' fields is missing or empty in the payload.")

            # 4. Use intermediate variables for clarity before instantiation.
            payload_dto = dtos.ShippingWebhookRequestDTO(
                #provider="easypost",
                tracking_reference=tracking_reference,
                tenant_id=tenant_id,
                status=status,
                occured_at=occurred_at,
                order_id=order_id,
                #raw_payload=payload
            )

            return payload_dto

            #return dtos.ShippingWebhookIntegrationEvent(
            #    event_type="webhook_events.ShippingTracker",
            #    data=payload_dto,
            #)

        except KeyError as e:
            # Handle missing mandatory fields gracefully
            raise Exception(f"Missing required key in EasyPost payload: {e}") from e
        except (TypeError, ValueError) as e:
            # Handle invalid data types or formats (e.g., bad date string)
            raise Exception(f"Invalid data format in EasyPost payload: {e}") from e

