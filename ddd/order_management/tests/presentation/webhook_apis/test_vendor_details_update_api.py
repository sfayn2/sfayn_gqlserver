import pytest, os, json, time
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
    vendor_details = dtos.VendorDetailsSnapshotDTO(
        vendor_id="v-234",
        tenant_id=tenant_id,
        name="Vendor1",
        country="Singapore",
        is_active=True
    )
    return commands.PublishVendorDetailsUpdateCommand(
        event_type="order_management.internal_events.VendorDetailsUpdatedEvent",
        data=vendor_details

    )


@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "364f990ba8904a307b6e25e9b83a15469d04637dac27f5c663c16ec670e7a520",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_details_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Details update has been published."}'
