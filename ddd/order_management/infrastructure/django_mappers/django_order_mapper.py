from __future__ import annotations
import ast, json
from typing import Dict, Any, List, Optional

from ddd.order_management.domain import value_objects, models, enums
from ddd.order_management.infrastructure import django_mappers
from order_management import models as django_snapshots


class OrderMapper:
    """
    Infrastructure layer mapper between Domain Order aggregate and Django ORM snapshot model.
    """

    @staticmethod
    def to_django(order: models.Order) -> Dict[str, Any]:
        """
        Converts a domain Order object into a dictionary format suitable 
        for Django ORM update_or_create operations (snapshotting the state).
        """
        return {
            'order_id': order.order_id,
            'defaults': {
                    'version': order._version,
                    'tenant_id': order.tenant_id, 
                    'external_ref': order.external_ref,
                    'customer_id': order.customer_details.customer_id, 
                    'customer_name': order.customer_details.name, 
                    'customer_email': order.customer_details.email,
                    'order_status': order.order_status.value, 
                    'payment_status': order.payment_status.value,
                    'currency': order.currency,
                    'date_created': order.date_created,
                    'date_modified': order.date_modified
                }
        }

    @staticmethod
    def to_domain(django_order_object: django_snapshots.Order) -> models.Order:
        """
        Converts a Django ORM snapshot object back into a rich domain Order aggregate.
        """
        
        customer_id: Optional[str] = django_order_object.customer_id
        customer_name = django_order_object.customer_name
        customer_email = django_order_object.customer_email

        return models.Order(
            _version=django_order_object.version,
            order_id=django_order_object.order_id,
            external_ref=django_order_object.external_ref,
            tenant_id=django_order_object.tenant_id, 
            date_created=django_order_object.date_created,
            date_modified=django_order_object.date_modified, 
            customer_details=value_objects.CustomerDetails(
                customer_id=customer_id, 
                name=customer_name, 
                email=customer_email
            ),
            line_items=[
                django_mappers.LineItemMapper.to_domain(item) 
                for item in django_order_object.line_items.all()
            ],
            shipments=[
                django_mappers.ShipmentMapper.to_domain(item) 
                for item in django_order_object.shipments.all()
            ],
            order_status=enums.OrderStatus(django_order_object.order_status),
            payment_status=enums.PaymentStatus(django_order_object.payment_status),
        )
