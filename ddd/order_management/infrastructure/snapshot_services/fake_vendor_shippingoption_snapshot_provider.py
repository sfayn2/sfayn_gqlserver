from __future__ import annotations
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeVendorShippingOptionSnapshotProvider(ports.VendorShippingOptionSnapshotAbstract):

    def get_all_shipping_options(self) -> List[dtos.VendorShippingOptionSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorShippingOptionSnapshotDTO(
                vendor_id="v-234",
                name="Standard",
                delivery_time="2-3 Days",
                conditions={"max_weight": 30},
                base_cost=Decimal("5"),
                flat_rate=Decimal("0.0"),
                currency="SGD",
                is_active=True
            )
        ]

