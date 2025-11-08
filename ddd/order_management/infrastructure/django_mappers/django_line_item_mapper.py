import ast, json
from typing import Any
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class LineItemMapper:

    @staticmethod
    def to_django(order_id: str, line_item: models.LineItem) -> dict:
        return {
                "product_sku": line_item.product_sku,
                "order_id": order_id,
                "defaults":  {
                    'product_sku': line_item.product_sku, 
                    'product_name': line_item.product_name, 
                    'product_price': line_item.product_price.amount, 
                    'product_currency': line_item.product_price.currency, 
                    'order_quantity': line_item.order_quantity, 
                    'vendor_id': line_item.vendor_id, 
                    'package_weight_kg': line_item.package.weight_kg,
                }
            }

    @staticmethod
    def to_domain(django_line_item: Any) -> models.LineItem:

        return models.LineItem(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            product_price=value_objects.Money(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            vendor_id=django_line_item.vendor_id,
            package=value_objects.Package(
                weight_kg=django_line_item.package_weight_kg
            )
            #options=json.loads(django_line_item.options),
        )
