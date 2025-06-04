from __future__ import annotations
import uuid
from typing import List, Union
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.domain import exceptions
from vendor_management import models as django_vendor_models

class DjangoProductsVendorValidationServiceAdapter(ports.ProductsVendorValidationServiceAbstract):

    def ensure_line_items_vendor_is_valid(self, items: List[models.LineItem]) -> None:
        for item in items:
            res = django_vendor_models.Vendor.objects.filter(id=item.vendor.id, name=item.vendor.name, country=item.vendor.country)
            if res.exists():
                django_mappers.VendorDetailsMapper.to_domain(res)
            else:
                raise exceptions.VendorNotFoundException(f"Vendor {item.vendor.name} not found.")
