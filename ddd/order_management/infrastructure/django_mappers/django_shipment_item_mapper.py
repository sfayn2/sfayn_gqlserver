import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models
from .django_line_item_mapper import LineItemMapper

class ShipmentItemMapper:

    @staticmethod
    def to_django(line_item_id, shipment_item: models.ShipmentItem) -> dict:
        return {
                "shipment_item_id": shipment_item.shipment_item_id,
                "defaults":  {
                    'shipment_id': shipment_item.shipment_id,
                    'quantity': shipment_item.quantity,
                    'allocated_shipping_tax': shipment_item.allocated_shipping_tax.amount,
                    'allocated_shipping_tax_currency': shipment_item.allocated_shipping_tax.currency
                }
            }

    def to_domain(django_shipment_item) -> models.ShipmentItem:

        return models.ShipmentItem(
            shipment_item_id=django_shipment_item.shipment_item_id,
            line_item=LineItemMapper.to_domain(django_shipment_item.line_item),
            quantity=django_shipment_item.quantity,
            allocated_shipping_tax=django_shipment_item.allocated_shipping_tax
        )
