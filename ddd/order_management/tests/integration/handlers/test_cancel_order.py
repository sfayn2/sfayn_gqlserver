import pytest, copy
from ddd.order_management.application import commands, handlers, dtos, ports
from ddd.order_management.domain import enums
from order_management import models as django_snapshots

# Use global constants defined in conftest.py (assumed to be in scope)



@pytest.mark.django_db
@pytest.mark.parametrize(
    "tenant_id, order_id, expected_success, expected_message",
    [
        (
            # Case 1: Success (Minimal valid input)
            "tenant_123",
            "ORD-CONFIRMED-1",
            True,
            "Order ORD-CONFIRMED-1 successfully canceled."
        ),
        (
            # Case 2: DRAFT cannot be cancel
            "tenant_123",
            "ORD-DRAFT-1",
            False,
            "Order in ORD-DRAFT-1 cannot be canceled."
        ),
        (
            # Case 2: w Shipments cannot be cancel
            "tenant_123",
            "ORD-CONFIRMED_W_SHIPPED-1",
            False,
            #"Cannot cancel, Shipments has already been shipped or delivered."
            "Order in ORD-CONFIRMED_W_SHIPPED-1 cannot be canceled."
        ),
    ]
)
def test_handle_cancel_order(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    fake_uow, # Real DjangoUOW
    tenant_id,
    order_id,
    expected_success,
    expected_message,
    django_db_blocker # Needed for post-assertion DB check
):
    
    
    # --- 1. Prepare Inputs & Context ---
    # Merge base input with any scenario-specific overrides
    input_data = {"order_id": order_id}

    # Setup Access Control Context (we need a valid user for the handler to run)
    access_control_service = fake_access_control
    access_control = access_control_service.create_access_control(tenant_id)
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, tenant_id)
    

    # --- 2. Execution (The SUT call) ---
    response = None
    try:
        # The Command DTO validates the input immediately
        command = commands.CancelOrderCommand.model_validate(input_data)
        
        # The handler consumes the command DTO and context
        response = handlers.handle_cancel_order(
            command=command,
            uow=fake_uow,
            access_control=access_control,
            user_ctx=user_ctx,
            exception_handler=fake_exception_handler,
            user_action_service=fake_user_action_service
        )
    except Exception as e:
        # Catch command validation errors (e.g., empty reason) that happen before handler execution
        assert not expected_success
        assert expected_message in str(e)
        return 

    # --- 3. Assertions (Only DTO outcome and message match) ---
    assert response is not None
    assert response.success is expected_success
    assert expected_message in response.message 

    # Optional: Integration-style verification of DB state for success cases
    if expected_success:
        with django_db_blocker.unblock(): 
             order_snapshot = django_snapshots.Order.objects.get(order_id=input_data['order_id'], tenant_id=tenant_id)
             assert order_snapshot.order_status == enums.OrderStatus.CANCELLED.value

