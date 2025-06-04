from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from vendor_management import models as django_vendor_models
from product_catalog import models as django_product_models

class DjangoProductsVendorValidationServiceAdapter(ports.ProductsVendorValidationServiceAbstract):

    def ensure_line_items_vendor_is_valid(self, items: List[models.LineItem]) -> None:
        for item in items:
            try:
                vendor = django_vendor_models.Vendor.objects.get(id=item.vendor.id)
            except django_vendor_models.DoesNotExist:
                raise exceptions.VendorNotFoundException(f"Vendor {item.vendor.id} not found.")

            try:
                product = django_product_models.VendorItem.objects.get(sku=item.product_sku, product__vendor_id=item.vendor.id)
            except django_product_models.DoesNotExist:
                raise exceptions.VendorNotFoundException(f"Product SKU {item.product_sku} is not owned by Vendor ID {item.vendor.id}.")

            # Fill in the missing vendor details
            item.vendor = value_objects.VendorDetails(
                id=vendor.id,
                name=vendor.name,
                country=vendor.country
            )
