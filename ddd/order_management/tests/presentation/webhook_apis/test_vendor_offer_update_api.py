import pytest, os, json, time
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse
from ddd.order_management.domain import enums
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
    vendor_offer = dtos.VendorOfferSnapshotDTO(
        vendor_id="v-234",
        offer_id="o-123",
        tenant_id="tenant123",
        offer_type=enums.OfferType.PERCENTAGE_DISCOUNT,
        name="10% Off",
        discount_value="10",
        conditions={"eligible_products": ["SKU1"]},
        required_coupon=False,
        stackable=True,
        priority=1,
        start_date=datetime(2025, 8, 13, 14, 30, 29, tzinfo=timezone.utc),
        end_date=datetime(2025, 12, 13, 14, 30, 29, tzinfo=timezone.utc),
        is_active=True
    )
    return commands.PublishVendorOfferUpdateCommand(
        event_type="order_management.internal_events.VendorOfferUpdatedEvent",
        data=vendor_offer

    )


@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "b75a8f2498dfb3dc77931ea565aad6cb4a375d07c399d3ed716c703266341d64",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_offer_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Offer update has been published."}'
