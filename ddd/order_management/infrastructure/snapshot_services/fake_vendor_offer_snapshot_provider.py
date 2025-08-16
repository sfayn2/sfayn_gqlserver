from __future__ import annotations
import pytz
import uuid
import json
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.domain import enums
from ddd.order_management.application import ports, dtos


class FakeVendorOfferSnapshotProvider(ports.VendorOfferSnapshotAbstract):

    def get_all_offers(self) -> List[dtos.VendorOfferSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorOfferSnapshotDTO(
                vendor_id="v-234",
                offer_id="o-234",
                tenant_id="tenant123",
                offer_type=enums.OfferType.PERCENTAGE_DISCOUNT,
                name="10% Off",
                discount_value="10",
                conditions=json.dumps({"eligible_products": ["SKU1"]}),
                required_coupon=False,
                stackable=True,
                priority=1,
                start_date=datetime.now(pytz.utc),
                end_date=datetime.now(pytz.utc) + relativedelta(years=1),
                is_active=True
            )
        ]


    def get_coupons_for_offers(self, offer_id: str) -> List[dtos.VendorCouponSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorCouponSnapshotDTO(
                vendor_id="v-234",
                offer_id="o-234",
                tenant_id="tenant123",
                coupon_code="WELCOME25",
                start_date=datetime.now(pytz.utc),
                end_date=datetime.now(pytz.utc) + relativedelta(years=1),
                is_active=True
            )
        ]