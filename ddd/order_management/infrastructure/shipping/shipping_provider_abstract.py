from __future__ import annotations
from typing import Protocol
from ddd.order_management.application import (
    dtos
)

class ShippingProviderAbstract(Protocol):
    def create_shipment(self, shipment, tenant_id: str) -> dtos.CreateShipmentResponseDTO: ...
    def is_self_delivery(self) -> bool: ...
