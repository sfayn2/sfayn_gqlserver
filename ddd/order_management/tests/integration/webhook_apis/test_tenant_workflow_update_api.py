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


@pytest.fixture
def provider():
    return "wss"

@pytest.fixture
def tenant_id():
    return "tenant123"

@pytest.fixture
def valid_payload():
    vendor_product = dtos.VendorProductSnapshotDTO(
            product_id="p-234",
            tenant_id="tenant123",
            vendor_id="v-234",
            product_sku="T-SHIRT-L",
            product_name="T Shirt Large Size",
            product_category="Men's T-Shirts",
            options={"Size": "M", "Color": "RED"},
            product_price=Decimal("1.5"),
            stock=10,
            product_currency="SGD",
            package_weight_kg=Decimal("2.1"),
            package_length_cm=10,
            package_width_cm=10,
            package_height_cm=10,
            is_active=True
    )
    return commands.PublishProductUpdateCommand(
        event_type="order_management.internal_events.ProductUpdatedEvent",
        data=vendor_product

    )

@pytest.fixture
def mock_request_factory():
    from django.test import RequestFactory
    return RequestFactory()

@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "a6a839d2d0a1011423edfc0994aab1f94e13a08b3ce9896a96f87281a3ebf207",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, provider, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_product_sync", args=[provider, tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Product update has been published."}'
