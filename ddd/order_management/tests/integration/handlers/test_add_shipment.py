import pytest, os, json, time, copy
from datetime import datetime
from decimal import Decimal # Import Decimal
from ddd.order_management.application import (
    commands,
    handlers,
    dtos,
    message_bus
)

BASE_SHIPMENT_INPUT = {
    "order_id": "ORD-CONFIRMED-1",
    "shipment_mode": "pickup",
    "shipment_provider": "easypost",
    "package_weight_kg": 1.5,
    "package_length_cm": 10.0,
    "package_width_cm": 5.0,
    "package_height_cm": 2.0,
    "pickup_address": {
        "line1": "123 Main St", "city": "Anytown", "state": "CA", "postal": 90210, "country": "USA",
    },
    "pickup_window_start": datetime(2025, 12, 1, 10, 0, 0).isoformat(),
    "pickup_window_end": datetime(2025, 12, 1, 12, 0, 0).isoformat(),
    "pickup_instructions": "Leave package on the porch.",
    "shipment_address": {
        "line1": "456 Oak Ave", "city": "Otherville", "state": "NY", "postal": 10001, "country": "USA",
    },
    "instructions": "Deliver with care.",
    # This part will change per test case
    "shipment_items": [
        {"product_sku": "SKU-A", "quantity": 1, "vendor_id": "vendor-1"},
        {"product_sku": "SKU-B", "quantity": 2, "vendor_id": "vendor-1"},
    ],
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "tenant_id, order_id, items_override, expected_success, expected_message",
    [
        (
            # tenant_id
            "tenant_123",
            "ORD-CONFIRMED-1",
            # Items Override (Original valid case)
            [
                {"product_sku": "SKU-A", "quantity": 1, "vendor_id": "vendor-1"},
                {"product_sku": "SKU-B", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            # expected_success
            True,
            # expected_message
            "Order ORD-CONFIRMED-1 successfully add new shipment."
        ),
        (
            "tenant_123",
            "ORD-CONFIRMED-1",
            [
                {"product_sku": "SKU-A", "quantity": 2, "vendor_id": "vendor-1"},
                {"product_sku": "SKU-B", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Cannot add shipment. Total allocated quantity (5) exceeds the order's total quantity (4)."
        ),
        (
            "tenant_123",
            "ORD-CONFIRMED-1",
            [
                {"product_sku": "SKU-NOTFOUND", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Vendor vendor-1 Line item w SKU SKU-NOTFOUND not found in order ORD-CONFIRMED-1"
        ),
        (
            "tenant_123",
            "ORD-NOTCONFIRMED-1",
            [
                {"product_sku": "SKU-NOTCONFIRMED", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Only confirm order can add shipment."
        ),
        # Add more test cases here
    ]
)
def test_add_shipment(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    fake_uow,
    domain_clock,
    tenant_id,
    order_id,
    items_override,
    expected_success,
    expected_message,
):

    input_data = copy.deepcopy(BASE_SHIPMENT_INPUT)
    
    # Override the specific part that changes
    input_data["order_id"] = order_id
    input_data["shipment_items"] = items_override

    access_control = fake_access_control().create_access_control(tenant_id)
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, tenant_id)

    command = commands.AddShipmentCommand.model_validate(input_data)

    response = handlers.handle_add_shipment(
        command=command,
        uow=fake_uow,
        access_control=access_control,
        user_ctx=user_ctx,
        exception_handler=fake_exception_handler,
        user_action_service=fake_user_action_service
    )


    assert response.success is expected_success
    assert response.message == expected_message



