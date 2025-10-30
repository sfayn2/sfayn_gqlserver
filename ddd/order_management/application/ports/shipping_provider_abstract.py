from __future__ import annotations
from typing import Protocol

class ShippingProviderAbstract(Protocol):
    def create_shipment(self, shipment) -> dtos.CreateShipmentResult:
        ...

    def is_self_delivery(self) -> bool:
        ...
