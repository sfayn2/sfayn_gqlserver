import pytest, os, json, time
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse







@pytest.mark.django_db
def test_valid_post_returns_200(generic_request_post_shipment_tracker_webhook):
    response = generic_request_post_shipment_tracker_webhook
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "Shipment updates have been published to queue."}'
