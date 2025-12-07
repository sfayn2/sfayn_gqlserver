import pytest, os, json, time
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse
from ddd.order_management.application import (
    dtos, 
    commands
)


@pytest.fixture
def tracker_data_dict():
    # The original Python dictionary you want to send in the POST request
    return {
        "tracking_number": "TN123456789",
        "status": "DELIVERED",
        "occurred_at": "2025-12-07T10:00:00Z",
    }


@pytest.fixture
def valid_payload(tracker_data_dict, custom_headers, test_constants):
    SAAS_ID = test_constants.get("saas1")


    json_string = json.dumps(tracker_data_dict) # Converts the dict to a JSON string
    encoded_tracker_data = json_string.encode("utf-8") # Now you can encode the string

    return commands.PublishShipmentTrackerCommand.model_validate(
            { "headers" : custom_headers,
              "raw_body": encoded_tracker_data,
              "request_path": "webhook/shipment-tracker",
              "saas_id": SAAS_ID
            }
        )


@pytest.fixture
def custom_headers():
    return {
        "HTTP_X_Wss_Signature": "d1f4101d6368bc38c2075bc4893293c71c61e0250c7eb8fd9c44d70a9c59906c",
        "HTTP_X_Wss_Timestamp": str(int(time.time()))
    }

@pytest.mark.django_db
def test_valid_post_returns_200(client, valid_payload, custom_headers, tracker_data_dict, test_constants):
    SAAS_ID = test_constants.get("saas1")
    response = client.post(
        reverse("shipment_tracker_webhook", args=[SAAS_ID]),
        data=tracker_data_dict,
        content_type="application/json",
        **custom_headers
    )
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Shipment updates have been published to queue."}'
