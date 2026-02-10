import pytest

@pytest.mark.django_db
def test_shipment_tracker_webhook_success(generic_request_post_shipment_tracker_webhook):
    response = generic_request_post_shipment_tracker_webhook
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Shipment updates have been published to queue."}'

