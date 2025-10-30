from __future__ import annotations
from decimal import Decimal
from ddd.order_management.application import dtos

#Protocol: ports.ShippingProviderAbstract
class FedExShippingProvider:
    name = "FedEx"

    def __init__(self, api_key: str, account_number: str, endpoint: str):
        self.api_key = api_key
        self.account_number = account_number
        self.endpoint = endpoint

    def is_self_delivery(self) -> bool:
        return False

    def create_shipment(self, shipment) -> dtos.CreateShipmentResult:
        payload = {
            "account_number": self.account_number,
            "items": [
                {"sku": i.product_sku, "quantity": i.quantity}
                for i in shipment.shipment_items
            ],
            "ship_to": shipment.shipment_address.to_dict()
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.endpoint}/shipments", json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        return dtos.CreateShipmentResult(
            "tracking_number": data["tracking_number"],
            "total_amount": dtos.Money(
                amount=Decimal(data["total_amount"]),
                currency=data["currency"]
            )
        )