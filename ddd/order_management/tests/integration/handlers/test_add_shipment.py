import pytest, os, json, time, copy
from datetime import datetime
from decimal import Decimal # Import Decimal
from ddd.order_management.application import (
    commands,
    handlers,
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state

BASE_SHIPMENT_INPUT = {
    "order_id": "ORD-CONFIRMED-1",
    "shipment_mode": "pickup",
    "shipment_provider": "easypost",
    "package_weight_kg": 1.5,
    "package_length_cm": 10.0,
    "package_width_cm": 5.0,
    "package_height_cm": 2.0,
    "pickup_address": {
        "line1": "123 Main St", "city": "Anytown", "state": "CA", "postal": "90210", "country": "USA",
    },
    "pickup_window_start": datetime(2025, 12, 1, 10, 0, 0).isoformat(),
    "pickup_window_end": datetime(2025, 12, 1, 12, 0, 0).isoformat(),
    "pickup_instructions": "Leave package on the porch.",
    "shipment_address": {
        "line1": "456 Oak Ave", "city": "Otherville", "state": "NY", "postal": "10001", "country": "USA",
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
    "order_id, items_override, expected_success, expected_message, expected_shipment_status_after",
    [
        (
            "ORD-CONFIRMED-1",
            # Items Override (Original valid case)
            [
                {"product_sku": "SKU-A", "quantity": 1, "vendor_id": "vendor-1"},
                {"product_sku": "SKU-B", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            # expected_success
            True,
            # expected_message
            "Order ORD-CONFIRMED-1 successfully add new shipment.",
            enums.ShipmentStatus.PENDING.value,
        ),
        (
            "ORD-CONFIRMED-1",
            [
                {"product_sku": "SKU-A", "quantity": 2, "vendor_id": "vendor-1"},
                {"product_sku": "SKU-B", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Cannot add shipment. Total allocated quantity (5) exceeds the order's total quantity (4).",
            None,
        ),
        (
            "ORD-CONFIRMED-1",
            [
                {"product_sku": "SKU-NOTFOUND", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Vendor vendor-1 Line item w SKU SKU-NOTFOUND not found in order ORD-CONFIRMED-1",
            None,
        ),
        (
            "ORD-NOTCONFIRMED-1",
            [
                {"product_sku": "SKU-NOTCONFIRMED", "quantity": 2, "vendor_id": "vendor-1"},
            ],
            False,
            "Only confirm order can add shipment.",
            None,
        ),
        # Add more test cases here
    ]
)
def test_add_shipment(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    test_constants,
    fake_uow,
    domain_clock,
    order_id,
    items_override,
    expected_success,
    expected_message,
    expected_shipment_status_after
):

    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")

    input_data = copy.deepcopy(BASE_SHIPMENT_INPUT)
    
    # Override the specific part that changes
    input_data["order_id"] = order_id
    input_data["shipment_items"] = items_override

    access_control = fake_access_control().create_access_control(TENANT1)
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

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


    # Verify the final state of the shipment in the database
    try:
        if expected_shipment_status_after: #only applies to success created
            django_shipment_snapshot = django_snapshots.Shipment.objects.get(
                shipment_id="SH-1",
                order_id=command.order_id
            )

            assert django_shipment_snapshot.shipment_status == expected_shipment_status_after

    except django_snapshots.Shipment.DoesNotExist:
        pytest.fail(f"Shipment {command.order_id} SH-1 not found in DB after operation.")

    if expected_shipment_status_after: #only applies to success created
        # Verify user action logging occurred only on success
        action_log_exists = django_snapshots.UserActionLog.objects.filter(
            order_id=command.order_id,
            action="add_shipment",
            performed_by=USER1
        ).exists()
        
        assert action_log_exists == expected_success

