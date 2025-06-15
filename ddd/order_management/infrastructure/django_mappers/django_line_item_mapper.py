import ast
from decimal import Decimal
from ddd.order_management.domain import value_objects, models

class LineItemMapper:

    @staticmethod
    def to_django(order_id, line_item: models.LineItem) -> dict:
        return {
                "product_sku": line_item.product_sku,
                "order_id": order_id,
                "defaults":  {
                    'product_name': line_item.product_name, 
                    'vendor_id': line_item.vendor.vendor_id, 
                    'vendor_name': line_item.vendor.name, 
                    'vendor_country': line_item.vendor.country, 
                    'product_category': line_item.product_category, 
                    'options': line_item.options, 
                    'product_price': line_item.product_price.amount, 
                    'product_currency': line_item.product_price.currency,
                    'order_quantity': line_item.order_quantity, 
                    'package_weight': line_item.package.weight,
                    'package_length': line_item.package.dimensions[0],
                    'package_width': line_item.package.dimensions[1],
                    'package_height': line_item.package.dimensions[2],
                    'is_free_gift': line_item.is_free_gift, 
                    'is_taxable': line_item.is_taxable
                }
            }

    def to_domain(django_line_item) -> models.LineItem:
        return models.LineItem(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            vendor=value_objects.VendorDetails(
                vendor_id=django_line_item.vendor_id,
                name=django_line_item.vendor_name,
                country=django_line_item.vendor_country
            ),
            product_category=django_line_item.product_category,
            options=ast.literal_eval(django_line_item.options),
            product_price=value_objects.Money(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            package=value_objects.Package(
                weight=Decimal(django_line_item.package_weight),
                dimensions=(
                    int(django_line_item.package_length), 
                    int(django_line_item.package_width), 
                    int(django_line_item.package_height)
                ) 
            ),
            is_free_gift=django_line_item.is_free_gift,
            is_taxable=django_line_item.is_taxable
        )
