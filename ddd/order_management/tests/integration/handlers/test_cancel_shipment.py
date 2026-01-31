import pytest, os, json, time, copy
from datetime import datetime, timezone
from decimal import Decimal
from ddd.order_management.application import (
    commands,
    handlers, # Assuming handlers.py contains handle_cancel_shipment
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state


# === Test Data from conftest/fixtures (assuming these are available) ===

# Order "ORD-CONFIRMED-1" has a PENDING shipment "SH-1".
BASE_CANCEL_SHIPMENT_INPUT = {
    "order_id": "ORD-CONFIRMED-1", 
    "shipment_id": "SH-1"
}

# Order "ORD-CONFIRMED_W_SHIPPED-1" has a SHIPPED shipment "SH-SHIPPED-2".
CANCEL_SHIPMENT_SHIPPED_INPUT = {
    "order_id": "ORD-CONFIRMED_W_SHIPPED-1",
    "shipment_id": "SH-SHIPPED-SHIPPED-2"
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_override, expected_success, expected_message_fragment, expected_shipment_status_after",
    [
        (
            # Valid cancellation of a PENDING shipment
            BASE_CANCEL_SHIPMENT_INPUT,
            True,
            "w Shipment Id SH-1 successfully shipped.",
            enums.ShipmentStatus.CANCELLED.value,
        ),
        (
            # Invalid cancellation of an already SHIPPED shipment
            CANCEL_SHIPMENT_SHIPPED_INPUT,
            False,
            "Cannot cancel shipment after in_transit/shipped/delivered", # Expecting domain exception message
            enums.ShipmentStatus.SHIPPED.value # Status should remain unchanged in DB
        ),
    ]
)
def test_cancel_shipment_handler(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    fake_uow,
    test_constants,
    domain_clock,
    input_override,
    expected_success,
    expected_message_fragment,
    expected_shipment_status_after
):
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")
    VENDOR1 = test_constants.get("vendor1")

    # --- Setup fixtures to match pattern ---
    input_data = copy.deepcopy(input_override)

    access_control_service = fake_access_control()
    access_control = access_control_service.create_access_control(TENANT1) 
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    # --- Execution ---
    command = commands.CancelShipmentCommand.model_validate(input_data)

    response = handlers.handle_cancel_shipment(
        command=command,
        uow=fake_uow,
        access_control=access_control,
        user_ctx=user_ctx,
        exception_handler=fake_exception_handler,
        user_action_service=fake_user_action_service
    )

    # --- Assertions ---
    assert response.success is expected_success
    assert expected_message_fragment in response.message
    
    # Verify the final state of the shipment in the database
    try:
        django_shipment_snapshot = django_snapshots.Shipment.objects.get(
            shipment_id=command.shipment_id,
            order_id=command.order_id
        )
        assert django_shipment_snapshot.shipment_status == expected_shipment_status_after
    except django_snapshots.Shipment.DoesNotExist:
        pytest.fail(f"Shipment {command.shipment_id} not found in DB after operation.")

    # Verify user action logging occurred only on success
    action_log_exists = django_snapshots.UserActionLog.objects.filter(
        order_id=command.order_id,
        action="cancel_shipment",
        performed_by=USER1
    ).exists()
    
    assert action_log_exists == expected_success
