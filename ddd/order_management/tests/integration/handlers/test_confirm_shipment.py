import pytest, os, json, time, copy
from datetime import datetime, timezone
from decimal import Decimal
from ddd.order_management.application import (
    commands,
    handlers, # Assuming handlers.py contains handle_confirm_shipment
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state


# === Test Data from conftest/fixtures (assuming these are available in your scope) ===
# Assuming constants like TENANT1, USER1 are available via test_constants fixture or global scope

# Order "ORD-CONFIRMED-1" has a PENDING shipment "SH-1".
BASE_CONFIRM_SHIPMENT_INPUT = {
    "order_id": "ORD-CONFIRMED-1", 
    "shipment_id": "SH-1" # This shipment is PENDING and can be confirmed/shipped
}

# Order "ORD-CONFIRMED_W_CONFIRMED-1" has a CONFIRMED shipment "SH-CONFIRMED-2".
CONFIRM_SHIPMENT_ALREADY_CONFIRMED_INPUT = {
    "order_id": "ORD-CONFIRMED_W_CONFIRMED-1",
    "shipment_id": "SH-CONFIRMED-2" # This shipment is already CONFIRMED
}



@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_override, expected_success, expected_message_fragment, expected_shipment_status_after",
    [
        (
            # Valid confirmation of a PENDING shipment
            BASE_CONFIRM_SHIPMENT_INPUT,
            True,
            "w Shipment Id SH-1 successfully confirmed.",
            enums.ShipmentStatus.CONFIRMED.value, # Status changes to CONFIRMED
        ),
        (
            # Invalid confirmation of an already CONFIRMED shipment
            CONFIRM_SHIPMENT_ALREADY_CONFIRMED_INPUT,
            False,
            "Only pending shipment can be confirm", # Expecting domain exception message for invalid state transition
            enums.ShipmentStatus.CONFIRMED.value # Status should remain unchanged in DB
        ),
    ]
)
def test_confirm_shipment_handler(
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
    # Retrieve constants from fixture
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")
    # VENDOR1 = test_constants.get("vendor1") # Not explicitly used here but available

    # --- Setup fixtures to match pattern ---
    input_data = copy.deepcopy(input_override)

    access_control_service = fake_access_control()
    access_control = access_control_service.create_access_control(TENANT1) 
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    # --- Execution ---
    command = commands.ConfirmShipmentCommand.model_validate(input_data)

    # Note: Replace 'handle_cancel_shipment' with 'handle_confirm_shipment' from your new request
    response = handlers.handle_confirm_shipment(
        command=command,
        uow=fake_uow,
        access_control=access_control,
        user_ctx=user_ctx,
        exception_handler=fake_exception_handler,
        user_action_service=fake_user_action_service,
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
        action="confirm_shipment", # Action name from the new handler
        performed_by=USER1
    ).exists()
    
    assert action_log_exists == expected_success
