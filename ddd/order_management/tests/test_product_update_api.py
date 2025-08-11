import pytest, os, json, time
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
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
        event_type="order_management.internal_events.ProductUpdateEvent",
        tenant_id="tenant123",
        data=vendor_product

    )

@pytest.fixture
def mock_request_factory():
    from django.test import RequestFactory
    return RequestFactory()

@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "44296d9b88e646dbea320498a96231a6d808faea21c482df82cfa9d39e2226c6",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

#@patch("ddd.order_management.presentation.webhook_apis.common.validate_webhook")
@patch("ddd.order_management.application.message_bus.handle")
#def test_valid_post_returns_200(mock_handle, mock_validate, mock_request_factory, provider, tenant_id, valid_payload, custom_headers):
def test_valid_post_returns_200(mock_handle, mock_request_factory, provider, tenant_id, valid_payload, custom_headers):

    #mock_validate.return_value = valid_payload
    mock_handle.return_value = dtos.ResponseDTO(
        success=True,
        message="Product update has been published."
    )

    request = mock_request_factory.post(
        f"/webhook/{provider}/{tenant_id}/product_update",
        data=valid_payload.model_dump_json(by_alias=True),
        content_type="application/json",
        **custom_headers
    )

    response = webhook_apis.product_update_api(request, provider, tenant_id)

    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Product update has been published."}'

    #mock_validate.assert_called_once()
    mock_handle.assert_called_once()
