import ast, json
from ddd.order_management.domain import value_objects, models, enums
from ddd.order_management.infrastructure import django_mappers
from order_management import models as django_snapshots

class OrderMapper:

    @staticmethod
    def to_django(order: models.Order):
        return {
            'order_id': order.order_id,
            'defaults': {
                    'tenant_id': order.tenant_id,
                    'external_ref': order.external_ref,
                    'customer_id': order.customer_details.customer_id, 
                    'customer_name': order.customer_details.customer_name, 
                    'customer_email': order.customer_details.customer_email,
                    'order_status': order.order_status.value, 
                    'payment_status': order.payment_status, 
                    'currency': order.currency,
                    'date_created': order.date_created,
                    'date_modified': order.date_modified
                }
        }

    @staticmethod
    def to_domain(django_order_object) -> models.Order:

        return models.Order(
            order_id=django_order_object.order_id,
            external_ref=django_order_object.external_ref,
            tenant_id=django_order_object.tenant_id,
            date_created=django_order_object.date_created,
            date_modified=django_order_object.date_modified, 
            customer_details=value_objects.CustomerDetails(
                customer_id=django_order_object.customer_id, 
                customer_name=django_order_object.customer_name, 
                customer_email=django_order_object.customer_email

            ),
            line_items=[
                django_mappers.LineItemMapper.to_domain(item) for item in django_order_object.line_items.all()
            ],
            shipments=[
                django_mappers.ShipmentMapper.to_domain(item) for item in django_order_object.shipments.all()
            ],
            order_status=django_order_object.order_status,
            payment_status=django_order_object.payment_status,
            currency=django_order_object.currency
        )

