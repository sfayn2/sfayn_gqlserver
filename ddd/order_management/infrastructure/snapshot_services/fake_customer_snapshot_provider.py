from __future__ import annotations
import pytz
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeCustomerSnapshotProvider(ports.CustomerSnapshotAbstract):

    def get_all_customers(self) -> List[dtos.CustomerDetailsSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.CustomerDetailsSnapshotDTO(
                customer_id="c-234",
                user_id=None,
                first_name="John",
                last_name="Doe",
                email="JohnDoe@gmail.com",
                is_active=True
            )
        ]


    def get_customer_address(self, customer_id: str) -> List[dtos.CustomerAddressSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.CustomerAddressSnapshotDTO(
                customer_id=customer_id,
                address_type="shipping",
                street="My street",
                city="City1",
                state="State1",
                postal=12345,
                country="USA",
                is_default=True,
                is_active=True
            )
        ]