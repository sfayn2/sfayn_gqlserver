from __future__ import annotations
from decimal import Decimal
from ddd.order_management.application import dtos

#Protocol: ports.ShippingProviderAbstract
class SelfDeliveryProvider:

    def is_self_delivery(self) -> bool:
        return True

    def create_shipment(self, shipment) -> dtos.CreateShipmentResult:
        raise NotImplementedError("Self delivery does not use external shipment creation.")
