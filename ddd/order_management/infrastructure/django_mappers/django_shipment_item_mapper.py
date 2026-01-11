import ast, json
from typing import Any
from decimal import Decimal
from ddd.order_management.domain import value_objects, models
from .django_line_item_mapper import LineItemMapper

class ShipmentItemMapper:

    @staticmethod
    def to_django(shipment_id: str, shipment_item: models.ShipmentItem) -> dict:
        return {
                "shipment_item_id": shipment_item.shipment_item_id,
                'shipment_id': shipment_id,
                "defaults":  {
                    "line_item_id": shipment_item.line_item.product_sku,
                    'quantity': shipment_item.quantity,
                }
            }

    @staticmethod
    def to_domain(django_shipment_item: Any) -> models.ShipmentItem:

        return models.ShipmentItem(
            shipment_item_id=django_shipment_item.shipment_item_id,
            line_item=LineItemMapper.to_domain(django_shipment_item.line_item),
            quantity=django_shipment_item.quantity,
        )
