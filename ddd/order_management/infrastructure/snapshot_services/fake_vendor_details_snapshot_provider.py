from __future__ import annotations
import pytz
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeVendorDetailsSnapshotProvider(ports.VendorDetailsSnapshotAbstract):

    def get_all_vendors(self) -> List[dtos.VendorDetailsSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorDetailsSnapshotDTO(
                vendor_id="v-234",
                name="Vendor1",
                country="Country1",
                is_active=True
            )
        ]

