import pytest, os, json, time
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse
from ddd.order_management.presentation import webhook_apis
from ddd.order_management.application import (
    dtos, 
    commands
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sfayn_gqlserver.settings')
import django
django.setup()


@pytest.fixture
def provider():
    return "wss"

@pytest.fixture
def tenant_id():
    return "tenant123"

@pytest.fixture
def valid_payload(tenant_id):
    vendor_coupon = dtos.VendorCouponSnapshotDTO(
        vendor_id="v-234",
        tenant_id=tenant_id,
        offer_id="o-123",
        coupon_code="WELCOME25",
        start_date=datetime(2025, 8, 13, 14, 30, 29, tzinfo=timezone.utc),
        end_date=datetime(2025, 10, 13, 14, 30, 29, tzinfo=timezone.utc),
        is_active=True
    )
    return commands.PublishVendorCouponUpdateCommand(
        event_type="order_management.internal_events.VendorCouponUpdatedEvent",
        data=vendor_coupon

    )


@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "c036dc6861fb5e9736eb594874072c920e8a77403b04e7f37e2f2742191336de",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_coupon_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Coupon update has been published."}'
