import ast, json
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class LineItemMapper:

    @staticmethod
    def to_django(order_id, line_item: models.LineItem) -> dict:
        return {
                "product_sku": line_item.product_sku,
                "order_id": order_id,
                "defaults":  {
                    'product_sku': line_item.product_sku, 
                    'product_name': line_item.product_name, 
                    'product_price': line_item.product_price.amount, 
                    'order_quantity': line_item.order_quantity, 
                    'vendor_name': line_item.vendor_name, 
                    'pickup_line1': line_item.pickup_address.line1,
                    'pickup_line2' : line_item.pickup_address.line2,
                    'pickup_city' : line_item.pickup_address.city,
                    'pickup_postal' : line_item.pickup_address.postal,
                    'pickup_country' : line_item.pickup_address.country,
                    'pickup_state': line_item.pickup_address.state
                }
            }

    def to_domain(django_line_item) -> models.LineItem:

        return models.LineItem(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            product_price=value_objects.Money(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            vendor_name=django_line_item.vendor_name,
            pickup_address=value_objects.Address(
                line1=django_line_item.pickup_address_line1,
                line2=django_line_item.pickup_address_line2,
                city=django_line_item.pickup_address_city,
                country=django_line_item.pickup_address_country,
                state=django_line_item.pickup_address_state,
                postal=django_line_item.pickup_address_postal
            )
            #options=json.loads(django_line_item.options),
        )
