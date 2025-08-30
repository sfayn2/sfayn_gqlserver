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
    vendor_payment = dtos.VendorPaymentOptionSnapshotDTO(
            vendor_id="v-234",
            tenant_id="tenant123",
            option_name="Pay by Paypal",
            conditions={},
            method="DIGITAL_WALLET",
            provider="paypal",
            is_active=True
    )
    return commands.PublishVendorPaymentOptionUpdateCommand(
        event_type="order_management.internal_events.VendorPaymentOptionUpdatedEvent",
        data=vendor_payment

    )


@pytest.fixture
def custom_headers(tenant_id):
    return {
        "HTTP_X_Wss_Signature": "3485b0487a449cb463b95d9fa03119cf3543db4aad72dd08dbd86bda13b34f35",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_vendor_paymentoption_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Vendor Payment Option update has been published."}'
