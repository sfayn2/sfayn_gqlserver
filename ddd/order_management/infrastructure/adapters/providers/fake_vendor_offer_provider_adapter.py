from __future__ import annotations
import uuid
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from ddd.order_management.doman import enums
from ddd.order_management.application import ports, dtos


class FakeVendorOffersProviderAdapter(ports.VendorOfferProviderAbstract):

    def get_all_offers(self) -> List[dtos.VendorOfferSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorOfferSnapshotDTO(
                vendor_id=uuid.uuid4(),
                offer_type=enums.OfferType["percentage_discount"],
                name="10% Off",
                discount_value="10",
                conditions={""},
                required_coupon=False,
                coupons=None,
                stackable=True,
                priority=1,
                start_date=datetime.now(),
                end_date=datetime.now() + relativedelta(years=1)
                is_active=True
            )
        ]


    def get_coupons_for_offers(vendor_id: uuid.UUID) -> List[dtos.VendorCouponSnapshotDTO]:
        #TODO rest api here
        return [
            dtos.VendorCouponSnapshotDTO(
                vendor_id=vendor_id,
                coupon_code="WELCOME25",
                start_date=datetime.now(),
                end_date=datetime.now() + relativedelta(years=1)
                is_active=True
            )
        ]