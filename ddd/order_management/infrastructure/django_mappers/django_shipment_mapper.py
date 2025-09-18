import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class ShipmentMapper:

    @staticmethod
    def to_django(order_id, shipment: models.Shipment) -> dict:
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
                    'shipment_service_code': shipment.shipment_service_code,
                    'tracking_reference': shipment.tracking_reference,
                    'shipment_amount': shipment.shipment_amount,
                    'shipment_tax_amount': shipment.shipment_tax_amount,
                    'shipment_status': shipment.shipment_status,
                }
        }

    def to_domain(django_shipment) -> models.LineItem:

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
            shipment_service_code=django_shipment.shipment_service_code,
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
                django_mappers.ShipmentLineItemMapper.to_domain(item) for item in django_shipment.shipment_items.all()
            ]
        )
