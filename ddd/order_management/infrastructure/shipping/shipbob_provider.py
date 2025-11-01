from __future__ import annotations
from typing import Any
from decimal import Decimal
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums
from .enums import ShippingProviderEnum

#Protocol: ports.ShippingProviderAbstract
class ShipBobShippingProvider:
    name = ShippingProviderEnums.SHIPBOB

    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")

    def is_self_delivery(self) -> bool:
        return False

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _format_pickup_window(self, shipment):
        return {
            "pickup_date": shipment.pickup_window_start.strftime("%Y-%m-%d"),
            "pickup_start_time": shipment.pickup_window_start.strftime("%H:%M"),
            "pickup_start_end": shipment.pickup_window_end.strftime("%H:%M")
        }


    def create_shipment(self, shipment) -> dtos.CreateShipmentResult:

        if shipment.shipment_method == enums.ShippingMethod.PICKUP:
            pickup_details = self._format_pickup_window(shipment)
        else:
            pickup_details = {}

        payload: dict[str, Any] = {
            "order_number": shipment.shipment_id,
            "to_address": as_dict(shipment.shipment_address),
            "pickup": pickup_details if shipment.shipment_method == enums.ShippingMethod.PICKUP else None,
            "items": [
                { "sku": i.product_sku, "quantity": i.quantity}
                for i in shipment.shipment_items
            ],
        }


        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.post(
                f"{self.endpoint}/orders", 
                json=payload, 
                headers=self._headers(),
                timeout=20
            )
            response.raise_for_status()
        except Exception as e:
            raise exceptions.ShippingProviderIntegrationError(f"{ShippingProviderEnum.SHIPBOB} request failed: {e}")

        data = response.json()

        return dtos.CreateShipmentResult(
            tracking_number=data.get("tracking_number") or data.get("id"),
            total_amount=dtos.Money(
                amount=data.get("shipping_cost", 0)
                currency=data.get("currency")
            ),
            label_url=data.get("label_url")
        )
    