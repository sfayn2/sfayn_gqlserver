import pytest


@pytest.mark.django_db
def test_valid_post_returns_200_tenant(generic_request_post_shipment_tracker_webhook_tenant):
    response = generic_request_post_shipment_tracker_webhook_tenant
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Shipment updates have been published to queue."}'

