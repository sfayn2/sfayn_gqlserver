from __future__ import annotations
from typing import List
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots
from ddd.order_management.domain import exceptions

class DjangoStockValidation(ports.StockValidationAbstract):

    def ensure_items_in_stock(self, tenant_id: str, skus: List[dtos.ProductSkusDTO] ) -> None:

        #if items:
        #    product_map = self._get_stocks(items, tenant_id)

        for item in skus:
            prod_snapshot = django_snapshots.VendorProductSnapshot.objects.filter(tenant_id=tenant_id, product_sku=item.product_sku, vendor_id=item.vendor_id)
            available_qty = None
            if prod_snapshot.exists():
                #available_qty = product_map.get(item.product_sku)
                available_qty = prod_snapshot.values_list("stock", flat=True)[0]
                if item.order_quantity > available_qty:
                    raise exceptions.OutOfStockException(f"Product {item.product_sku} has only {available_qty} remaining stock/s.")

            if available_qty is None:
                raise exceptions.OutOfStockException(f"Product {item.product_sku} is not known.")

    #def _get_stocks(self, items: List[models.LineItem], tenant_id: str):
    #    import pdb;pdb.set_trace()
    #    product_map = {
    #        p.product_sku: p.stock
    #        for p in django_snapshots.VendorProductSnapshot.objects.filter(tenant_id=tenant_id, product_sku__in=[item.product_sku for item in items], vendor_id=items[0].vendor.vendor_id)
    #    }

    #    return product_map


