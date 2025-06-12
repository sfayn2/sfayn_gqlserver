from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from order_management import models as django_snapshots

class DjangoProductsVendorValidationService(ports.ProductsVendorValidationServiceAbstract):

    def ensure_line_items_vendor_is_valid(self, items: List[models.LineItem]) -> None:
        for item in items:
            try:
                vendor_details_snapshot = django_snapshots.VendorDetailsSnapshot.objects.get(id=item.vendor.id)
            except django_snapshots.VendorDetailsSnapshot.DoesNotExist:
                raise exceptions.VendorNotFoundException(f"Vendor {item.vendor.id} not found.")

            try:
                product = django_snapshots.VendorProductSnapshot.objects.get(product_sku=item.product_sku, vendor_id=item.vendor.id)
            except django_product_models.DoesNotExist:
                raise exceptions.VendorNotFoundException(f"Product SKU {item.product_sku} is not owned by Vendor ID {item.vendor.id}.")

            # Fill in the missing vendor details
            item.vendor = value_objects.VendorDetails(
                id=vendor.id,
                name=vendor.name,
                country=vendor.country
            )
