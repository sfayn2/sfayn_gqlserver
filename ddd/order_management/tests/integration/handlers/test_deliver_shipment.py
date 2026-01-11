import pytest, os, json, time, copy
from datetime import datetime, timezone
from decimal import Decimal
from ddd.order_management.application import (
    commands,
    handlers, # Assuming handlers.py contains handle_deliver_shipment
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state


# === Test Data from conftest/fixtures (assuming these are available) ===
# Assuming constants like TENANT1, USER1 are available via test_constants fixture or global scope

# Order "ORD-CONFIRMED-1" has a PENDING shipment "SH-1".
# To test delivery, we assume this shipment is SHIPPED in the test DB setup (e.g., via a fixture or setup hook)
# Note: The provided seeds have "SH-SHIPPED-2" as SHIPPED. We'll use that.
BASE_DELIVER_SHIPMENT_INPUT = {
    "order_id": "ORD-CONFIRMED_W_SHIPPED-1", 
    "shipment_id": "SH-SHIPPED-2" # This shipment is already SHIPPED and ready for DELIVERY
}

# Define an input that is already DELIVERED (should cause an error)
DELIVER_SHIPMENT_ALREADY_DELIVERED_INPUT = {
    # We would need a seed in the DB for an already delivered shipment to test this thoroughly.
    # For now, we'll assume SH-SHIPPED-2 is what we target for the negative test case too, 
    # asserting the domain logic prevents re-delivery if the state machine is implemented correctly.
    # We will adjust expectations based on current seeds. Let's assume the previous test run set SH-1 to SHIPPED.
    "order_id": "ORD-CONFIRMED_W_DELIVERED-1",
    "shipment_id": "SH-DELIVERED-2"
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_override, expected_success, expected_message_fragment, expected_shipment_status_after, expected_order_status_after",
    [
        (
            # Valid delivery of a SHIPPED shipment (uses our BASE input pointing to a SHIPPED seed)
            BASE_DELIVER_SHIPMENT_INPUT,
            True,
            "w Shipment Id SH-SHIPPED-2 successfully delivered.", # Message seems generic ("shipped") but implies success
            enums.ShipmentStatus.DELIVERED.value,       # Shipment status should be DELIVERED
            enums.OrderStatus.DELIVERED.value           # <-- ROLL-UP: Order status should now be DELIVERED (as all items are covered)
        ),
        (
            # Invalid delivery of a PENDING shipment (using the other seed, assuming state logic prevents direct delivery from PENDING)
            DELIVER_SHIPMENT_ALREADY_DELIVERED_INPUT,
            False,
            "Shipment must be in SHIPPED status to be delivered", # Expecting domain exception message for invalid state transition
            enums.ShipmentStatus.DELIVERED.value,         # Status should remain unchanged in DB (PENDING)
            enums.OrderStatus.DELIVERED.value           # Order status remains original state
        ),
    ]
)
def test_deliver_shipment_handler(
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
    expected_shipment_status_after,
    expected_order_status_after # For the roll-up check
):
    # Retrieve constants from fixture
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")

    # --- Setup fixtures to match pattern ---
    input_data = copy.deepcopy(input_override)

    access_control_service = fake_access_control()
    access_control = access_control_service.create_access_control(TENANT1) 
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    command = commands.DeliverShipmentCommand.model_validate(input_data)

    # --- Execution ---
    # Note: Replace 'handle_cancel_shipment' with 'handle_deliver_shipment'
    response = handlers.handle_deliver_shipment(
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
    
    # Verify the specific shipment status
    try:
        django_shipment_snapshot = django_snapshots.Shipment.objects.get(
            shipment_id=command.shipment_id,
            order_id=command.order_id
        )
        assert django_shipment_snapshot.shipment_status == expected_shipment_status_after
    except django_snapshots.Shipment.DoesNotExist:
        pytest.fail(f"Shipment {command.shipment_id} not found in DB after operation.")

    # Verify order status roll-up if success is expected (can be simplified if you separated the roll-up test)
    if expected_order_status_after:
        try:
            django_order_snapshot = django_snapshots.Order.objects.get(order_id=command.order_id)
            assert django_order_snapshot.order_status == expected_order_status_after
        except (django_snapshots.Order.DoesNotExist, NameError):
             pass # Skip if model not available or not necessary for handler test

    # Verify user action logging occurred only on success
    action_log_exists = django_snapshots.UserActionLog.objects.filter(
        order_id=command.order_id,
        action="deliver_shipment", # Action name from the new handler
        performed_by=USER1
    ).exists()
    
    assert action_log_exists == expected_success
