from __future__ import annotations
from typing import List
from ddd.order_management.application import ports
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions

class DjangoStockValidation(ports.StockValidationAbstract):

    def ensure_items_in_stock(self, tenant_id: str, items: List[models.LineItem]) -> None:

        if items:
            product_map = self._get_stocks(items)

        for item in items:
            available_qty = product_map.get(item.product_sku)
            if available_qty is None or item.order_quantity > available_qty:
                raise exceptions.OutOfStockException(f"Product {item.product_sku} has only {available_qty} remaining stock/s.")

    def _get_stocks(self, items: List[models.LineItem]):
        product_map = {
            p.product_sku: p.stock
            for p in django_snapshots.VendorProductSnapshot.objects.filter(tenant_id=tenant_id, product_sku__in=[item.product_sku for item in items], vendor_id=items[0].vendor.vendor_id)
        }

        return product_map


