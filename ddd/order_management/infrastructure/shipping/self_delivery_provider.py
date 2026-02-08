from __future__ import annotations
from decimal import Decimal
from ddd.order_management.application import dtos

#Protocol: ports.ShippingProviderAbstract
class SelfDeliveryProvider:

    def create_shipment(self, shipment, tenant_id: str) -> dtos.CreateShipmentResponseDTO:
        tracking_code = f"SELF-{shipment.shipment_id}"
        label_url = None
        total_amount = Decimal("0.00")
        return dtos.CreateShipmentResponseDTO(
            tracking_reference=tracking_code,
            total_amount=dtos.MoneyResponseDTO(
                amount=total_amount,
                currency=shipment.currency
            ),
            label_url=label_url
        )
