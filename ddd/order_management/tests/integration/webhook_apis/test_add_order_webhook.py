import pytest, os, json, time
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse
from ddd.order_management.application import (
    dtos, 
    commands
)


@pytest.mark.django_db
def test_add_order_webhook_success(generic_request_post_add_order_webhook):
    response = generic_request_post_add_order_webhook
    assert response.status_code == 200
    assert response.content == b'{"success": true, "message": "New order has been publish to queue."}'