from __future__ import annotations
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeVendorProductSnapshotProvider(ports.VendorProductSnapshotAbstract):

    def get_all_products(self) -> List[dtos.VendorProductSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorProductSnapshotDTO(
                product_id="p-234",
                vendor_id="v-234",
                product_sku="T-SHIRT-L",
                product_name="T Shirt Large Size",
                product_category="Men's T-Shirts",
                options={"Size": "M", "Color": "RED"},
                product_price=Decimal("1.5"),
                stock=10,
                product_currency="SGD",
                package_weight=Decimal("2.1"),
                package_length=10,
                package_width=10,
                package_height=10,
                is_active=True
            )
        ]

