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
    return "tenant_123"

@pytest.fixture
def valid_payload(tenant_id):

    order_to_add = {
        "external_ref": "EXT-REF-123",
        "customer_details": {
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
        "product_skus": [
            {
                "product_sku": "SKU-PROD-A", 
                "order_quantity": 1, 
                "vendor_id": "vendor-1",
                "product_name": "Product A",
                "product_price": {"amount": Decimal("10.00"), "currency": "USD"},
                "package": {"weight_kg": Decimal("0.5")},
            },
            {
                "product_sku": "SKU-PROD-B", 
                "order_quantity": 2, 
                "vendor_id": "vendor-1",
                "product_name": "Product B",
                "product_price": {"amount": Decimal("5.00"), "currency": "USD"},
                "package": {"weight_kg": Decimal("0.25")},
            },
        ],
    }

    return commands.PublishAddOrderCommand(
        event_type="order_management.internal_events.AddOrderEvent",
        tenant_id=tenant_id,
        data=order_to_add
    )

@pytest.fixture
def mock_request_factory():
    from django.test import RequestFactory
    return RequestFactory()

@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "3d28d82da7abd22a0976a61f74a834294c28ca0c8f5ee1e8cd04b42dc391077a",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, tenant_id, valid_payload, custom_headers):
    response = client.post(
        reverse("tenant_webhook_tenant_add_order_sync", args=[tenant_id]),
        data=valid_payload.model_dump_json(),
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "New order has been publish to queue."}'
