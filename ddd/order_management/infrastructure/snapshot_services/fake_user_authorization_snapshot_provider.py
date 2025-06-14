from __future__ import annotations
import pytz
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeUserAuthorizationSnapshotProvider(ports.UserAuthorizationSnapshotAbstract):

    def get_all_users_auth(self) -> List[dtos.UserAuthorizationSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.UserAuthorizationSnapshotDTO(
                user_id=uuid.uuid4(),
                permission_codename="place_order",
                scope={"vendor_id": "v-123"},
                is_active=True
            )
        ]

