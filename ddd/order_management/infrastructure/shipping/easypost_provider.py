from __future__ import annotations
from typing import Any
from decimal import Decimal
from dataclasses import asdict
from ddd.order_management.application import dtos

#Protocol: ports.ShippingProviderAbstract
class EasyPostShippingProvider:
    name = "EasyPost"

    def __init__(self, api_key: str, endpoint: str = "https://api.easypost.com/v2"):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")

    def is_self_delivery(self) -> bool:
        return False

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_shipment(self, shipment) -> dtos.CreateShipmentResult:
        from_address = None
        if shipment.shipment_items:
            first_item = shipment.shipment_items[0]
            if hasattr(first_item, "pickup_address"):
                from_address = first_item.pickup_address

        payload: dict[str, Any] = {
            # optional: can be grabbed from line item pickup address
            "from_address": from_address,
            "to_address": as_dict(shipment.shipment_address),
            "parcel": self._build_parcel_payload(shipment),
            "options": {}
        }

        # add metadata for debugging
        payload["metadata"] = {
            "shipment_id": shipment.shipment_id,
            "item_count": len(shipment.shipment_items)
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.post(
                f"{self.endpoint}/shipments", 
                json=payload, 
                headers=self._headers(),
                timeout=20
            )
            response.raise_for_status()
        except Exception as e:
            raise exceptions.DomainIntegrationError(f"EasyPost request failed: {e}")

        data = response.json()

        rate_info = self._select_rate(data)
        total_amount = rate_info["amount"]
        currency = rate_info["currency"]

        #Easy post request explicit buy step to dispatch
        tracking_number, label_url = self._buy_shipment(data["id"], rate_info["id"])

        return dtos.CreateShipmentResult(
            tracking_number=tracking_number,
            total_amount=dtos.Money(
                amount=total_amount,
                currency=currency
            ),
            label_url=label_url
        )
    
    def _build_parcel_payload(self, shipment):

        total_weight = sum(
            si.package
            for si in shipment.shipment_items.line_item.package
        )

        length, width, height = shipment.get_max_dimension()
        parcel = {
            "weight": total_weight,
            "length": length,
            "width": width,
            "height": height
        }

    def _select_rate(self, data: dict[str, Any]) -> dict[str, Any]:
        rates = data.get("rates", [])
        if not rates:
            raise exceptions.DomainIntegrationError("No shipping rates returned from EasyPost.")

        selected = next((r for r in rates if r.get("selected")), None)
        candidate = selected or min(rates, key=lambda r: Decimal(r.get("rate") or "0"))

        return {
            "id": candidate.get("id"),
            "amount": Decimal(candidate.get("rate") or "0"),
            "currency": candidate.get("currency")
        }

    def _buy_shipment(self, shipment_id: str, rate_id: str) -> str:
        try:
            resp = request.post(
                f"{self.endpoint}/shipments/{shipment_id}/buy",
                json={"rate": {"id": rate_id}},
                headers=self._headers(),
                timeout=20
            )
            resp.raise_for_status()
        except request.RequestException as e:
            raise exceptions.DomainIntegrationError(f"EasyPost shipment buy failed: {e}")

        buy_data = resp.json()
        tracker = buy_data.get("tracker", {})
        tracking_code = tracker.get("tracking_code") or buy_data.get("tracking_code")

        label_url = buy_data.get("postage_label").get("label_url")

        if not tracking_code:
            raise exceptions.DomainIntegrationError(f"Missing tracking code after EasyPost buy step.")
        
        return tracking_code, label_url

       
       
       