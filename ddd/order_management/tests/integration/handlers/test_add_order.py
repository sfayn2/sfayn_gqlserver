import pytest, os, json, time, copy, re
from datetime import datetime
from decimal import Decimal
from ddd.order_management.application import (
    commands,
    handlers,
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions, enums
from order_management import models as django_snapshots # For verifying DB state

# Base input data for creating an order, matching the new DTO structure
BASE_ORDER_INPUT = {
    "external_ref": "EXT-REF-123",
    "tenant_id": "tenant_123",
    "customer_details": {
        "name": "John Doe",
        "email": "john.doe@example.com",
    },
    "product_skus": [
        {
            "product_sku": "SKU-PROD-A", 
            "order_quantity": 1, 
            "vendor_id": "vendor-1",
            "product_name": "Product A",
            "product_price": {"amount": Decimal("10.00"), "currency": "USD"},
            "package": {"weight_kg": Decimal("0.5")},
        },
        {
            "product_sku": "SKU-PROD-B", 
            "order_quantity": 2, 
            "vendor_id": "vendor-1",
            "product_name": "Product B",
            "product_price": {"amount": Decimal("5.00"), "currency": "USD"},
            "package": {"weight_kg": Decimal("0.25")},
        },
    ],
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_skus_override, expected_success, expected_message, expected_order_status_after",
    [
        (
            # Items Override (Original valid case)
            BASE_ORDER_INPUT["product_skus"],
            # expected_success
            True,
            # expected_message
            "successfully created.",
            enums.OrderStatus.CONFIRMED.value
        ),
        (
            # Invalid case: quantity <= 0 (assuming domain logic prevents this)
            [
                 {
                    "product_sku": "SKU-PROD-C", 
                    "order_quantity": 0, # Invalid quantity
                    "vendor_id": "vendor-1",
                    "product_name": "Product C",
                    "product_price": {"amount": Decimal("1.00"), "currency": "USD"},
                    "package": {"weight_kg": Decimal("0.1")},
                },
            ],
            False,
            # Message from domain exception (e.g., InvalidOrderOperation)
            "Order quantity must be greater than zero.",
            None
        ),
        (
            # Invalid case: Different currencies in the same order (assuming domain logic prevents this)
            [
                 {
                    **BASE_ORDER_INPUT["product_skus"][0], # Copy item 0 details
                    "product_price": {"amount": Decimal("10.00"), "currency": "EUR"}, # Different currency
                },
                 {
                    **BASE_ORDER_INPUT["product_skus"][1], # Copy item 1 details
                    "product_price": {"amount": Decimal("5.00"), "currency": "USD"}, # Original currency
                },
            ],
            False,
            "All line items must have the same currency.", # Assuming this domain validation exists
            None
        ),
        # Add more test cases for validation failures as needed
    ]
)
def test_add_order(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    fake_uow,
    domain_clock,
    test_constants,
    product_skus_override,
    expected_success,
    expected_message,
    expected_order_status_after
):
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")

    # Use deepcopy to avoid modifying the global BASE_ORDER_INPUT across tests
    input_data = copy.deepcopy(BASE_ORDER_INPUT)
    
    # Override the specific part that changes
    input_data["product_skus"] = product_skus_override
    input_data["tenant_id"] = TENANT1

    access_control_mock = fake_access_control()
    
    
    # Create the access control instance
    access_control = access_control_mock.create_access_control(TENANT1)
    # The user context mock needs to match the TENANT1 being tested
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    # --- Execution ---
    # The command should validate the input data structure
    command = commands.AddOrderCommand.model_validate(input_data)

    response = handlers.handle_add_order(
        command=command,
        uow=fake_uow,
        access_control=access_control,
        user_ctx=user_ctx,
        exception_handler=fake_exception_handler,
        user_action_service=fake_user_action_service
    )


    # --- Assertions ---
    assert response.success is expected_success
    # Use 'in' check for dynamic messages like "Order {order_id} successfully created."
    assert expected_message in response.message 

    # extract order id from response message
    order_id_from_response = response.message.split()[1]


    # Verify the final state of the shipment in the database
    try:
        if expected_order_status_after: #only applies to success created
            django_order_snapshot = django_snapshots.Order.objects.get(
                order_id=order_id_from_response
            )

            assert django_order_snapshot.order_status == expected_order_status_after

    except django_snapshots.Order.DoesNotExist:
        pytest.fail(f"Shipment {order_id_from_response} not found in DB after operation.")

    if expected_order_status_after: #only applies to success created
        # Verify user action logging occurred only on success
        action_log_exists = django_snapshots.UserActionLog.objects.filter(
            order_id=order_id_from_response,
            action="add_order",
            performed_by=USER1
        ).exists()

        assert action_log_exists == expected_success

