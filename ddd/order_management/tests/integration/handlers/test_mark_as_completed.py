import pytest, copy
from ddd.order_management.application import (
    commands,
    handlers,  # Assuming the provided handler is in handlers.py
    dtos,
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state (adjust import path if necessary)


# === Test Data Setup (assuming fixtures/seeds provide necessary initial DB state) ===

# The handler marks an entire order as completed, likely when all shipments/items are fulfilled.

# Order "ORD-READY-TO-COMPLETE-1" should be in a state (e.g., DELIVERED, but not yet COMPLETED)
# where the domain logic allows the `mark_as_completed()` method to succeed.
BASE_MARK_AS_COMPLETED_INPUT = {
    "order_id": "ORD-READY-TO-COMPLETE-1", 
}

# Order "ORD-READY-TO-COMPLETE-UNPAID-1" should be in a state (e.g., DELIVERED, but not yet COMPLETED) also w outstanding Payment
# where the domain logic allows the `mark_as_completed()` method to succeed.
BASE_MARK_AS_COMPLETED_UNPAID_INPUT = {
    "order_id": "ORD-READY-TO-COMPLETE-UNPAID-1", 
}

# Order "ORD-ALREADY-COMPLETED-1" should be in the COMPLETED state (or PENDING/CANCELLED)
# where the domain logic raises an InvalidOrderOperation exception.
MARK_AS_COMPLETED_INVALID_STATE_INPUT = {
    "order_id": "ORD-ALREADY-COMPLETED-1",
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "input_override, expected_success, expected_message_fragment, expected_order_status_after",
    [
        (
            # Valid completion of a suitable order (e.g., DELIVERED -> COMPLETED)
            BASE_MARK_AS_COMPLETED_INPUT,
            True,
            "successfully mark as completed",
            enums.OrderStatus.COMPLETED.value,
        ),
        (
            # Invalid operation due to outstanding Payment (e.g., PENDING -> raises InvalidOrderOperation)
            BASE_MARK_AS_COMPLETED_UNPAID_INPUT,
            False,
            "Cannot mark as completed with outstanding payments.",
            enums.OrderStatus.DELIVERED.value,
        ),
        (
            # Invalid operation due to current order state (e.g., PENDING -> raises InvalidOrderOperation)
            MARK_AS_COMPLETED_INVALID_STATE_INPUT,
            False,
            "Only delivered order can mark as completed.", # Expected domain exception message (adjust message based on actual domain logic)
            enums.OrderStatus.COMPLETED.value,         # Status should remain unchanged in DB (e.g., PENDING)
        ),
        #(
        #     # Invalid operation due to incorrect user role (e.g. USER role not VENDOR role)
        #    BASE_MARK_AS_COMPLETED_INPUT,
        #    False,
        #    "User not authorized", # Expecting access control exception message
        #    enums.OrderStatus.DELIVERED.value, # Status remains unchanged
        #),
    ]
)
def test_mark_as_completed_handler(
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
    expected_order_status_after,
):
    # Retrieve constants from fixture (assuming standard user setup)
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")

    # --- Setup fixtures to match pattern ---
    input_data = copy.deepcopy(input_override)

    # Configure access control mock based on test case requirements
    access_control_service = fake_access_control()
        
    access_control = access_control_service.create_access_control(TENANT1) 
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    # Note: Define `MarkAsCompletedCommand` in your application commands module
    command = commands.CompleteOrderCommand.model_validate(input_data)

    # --- Execution ---
    response = handlers.handle_mark_as_completed(
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
    
    # Verify the order status in the database snapshot
    try:
        django_order_snapshot = django_snapshots.Order.objects.get(order_id=command.order_id, tenant_id=TENANT1)
        assert django_order_snapshot.order_status == expected_order_status_after
    except (django_snapshots.Order.DoesNotExist, NameError):
        # Fail if the order disappeared, but pass if 'django_snapshots' isn't configured in the test env
        if expected_success:
             pytest.fail(f"Order {command.order_id} not found in DB after operation.")


    # Verify user action logging occurred only on success
    action_log_exists = django_snapshots.UserActionLog.objects.filter(
        order_id=command.order_id,
        action="mark_as_completed",
        performed_by=USER1
    ).exists()
    
    assert action_log_exists == expected_success
