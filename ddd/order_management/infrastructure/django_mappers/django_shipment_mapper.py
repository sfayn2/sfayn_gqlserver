from typing import Any
import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models
from ddd.order_management.infrastructure import django_mappers

class ShipmentMapper:

    @staticmethod
    def to_django(order_id: str, shipment: models.Shipment) -> dict:
        return {
                "shipment_id": shipment.shipment_id,
                "order_id": order_id,
                "defaults":  {
                    'shipment_address_line1': shipment.shipment_address.line1,
                    'shipment_address_line2' : shipment.shipment_address.line2,
                    'shipment_address_city': shipment.shipment_address.city,
                    'shipment_address_postal': shipment.shipment_address.postal,
                    'shipment_address_country' : shipment.shipment_address.country,
                    'shipment_address_state' : shipment.shipment_address.state,
                    'shipment_provider': shipment.shipment_provider,
                    'tracking_reference': shipment.tracking_reference,
                    'shipment_amount': shipment.shipment_amount.amount,
                    'shipment_currency': shipment.shipment_amount.currency,
                    'shipment_tax_amount': shipment.shipment_tax_amount.amount,
                    'shipment_status': shipment.shipment_status,
                }
        }

    @staticmethod
    def to_domain(django_shipment: Any) -> models.Shipment:

        return models.Shipment(
            shipment_id=django_shipment.shipment_id,
            shipment_address=value_objects.Address(
                line1=django_shipment.shipment_address_line1,
                line2=django_shipment.shipment_address_line2,
                country=django_shipment.shipment_address_country,
                city=django_shipment.shipment_address_city,
                postal=django_shipment.shipment_address_postal,
                state=django_shipment.shipment_address_state,
            ),
            shipment_provider=django_shipment.shipment_provider,
            tracking_reference=django_shipment.tracking_reference,
            shipment_amount=value_objects.Money(
                amount=django_shipment.shipment_amount,
                currency=django_shipment.shipment_currency
            ),
            shipment_tax_amount=value_objects.Money(
                amount=django_shipment.shipment_tax_amount,
                currency=django_shipment.shipment_currency
            ),
            shipment_status=django_shipment.shipment_status,
            shipment_items=[
                django_mappers.ShipmentItemMapper.to_domain(item) for item in django_shipment.shipment_items.all()
            ]
        )
