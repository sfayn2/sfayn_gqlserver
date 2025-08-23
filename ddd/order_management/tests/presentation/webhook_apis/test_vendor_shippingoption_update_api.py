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
    vendor_shipping = dtos.VendorShippingOptionSnapshotDTO(
            vendor_id="v-234",
            tenant_id="tenant123",
            option_name="MyStandard",
            method="STANDARD",
            provider="default",
            delivery_time="2-3 Days",
            conditions={"max_weight": 30},
            base_cost=Decimal("5"),
            flat_rate=Decimal("0.0"),
            currency="SGD",
            is_active=True
    )
    return commands.PublishVendorShippingOptionUpdateCommand(
        event_type="order_management.internal_events.VendorShippingOptionUpdatedEvent",
        data=vendor_shipping

    )


@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "951b13a3c5c9608b052409b831e7936c824678c14a925e32c0e5fad17f49b554",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_shippingoption_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Shipping Option update has been published."}'
