from __future__ import annotations
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class ShipmentItemMapper:

    @staticmethod
    def to_domain(shipment_item: dtos.ShipmentItemDTO) -> models.ShipmentItem:
        return models.ShipmentItem(
            product_sku=shipment_item.product_sku,
            quantity=shipment_item.quantity,
            vendor_id=shipment_item.vendor_id
        )