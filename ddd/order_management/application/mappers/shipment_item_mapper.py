from __future__ import annotations
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class ShipmentItemMapper:

    @staticmethod
    def to_domain(shipment_item: dtos.ShipmentItemDTO, line_item) -> models.ShipmentItem:

        return models.ShipmentItem(
            line_item=line_item,
            quantity=shipment_item.quantity
        )