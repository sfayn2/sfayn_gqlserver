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
    vendor_tax = dtos.VendorTaxOptionSnapshotDTO(
            vendor_id="v-234",
            tenant_id="tenant123",
            tax_type="GST",
            inclusive=False,
            provider="paypal",
            conditions={"country": "singapore"},
            rate=Decimal("0.07"),
            is_active=True
    )
    return commands.PublishVendorTaxOptionUpdateCommand(
        event_type="order_management.internal_events.VendorTaxOptionUpdatedEvent",
        data=vendor_tax

    )


@pytest.fixture
def custom_headers(tenant_id):
    return {
        "HTTP_X_Wss_Signature": "29362ae5df1db2a11f96a9a1c7ea2dbfcbbc5c99366157aca2b945995e4273d6",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_taxoption_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Tax Option update has been published."}'
