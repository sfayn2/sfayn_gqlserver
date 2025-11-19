import pytest, os, json, time, copy
from datetime import datetime
from decimal import Decimal
from ddd.order_management.application import (
    commands,
    handlers,
    dtos,
    message_bus
)
from ddd.order_management.domain import exceptions # Import the expected exceptions

# Base input data for creating an order, matching the new DTO structure
BASE_ORDER_INPUT = {
    "external_ref": "EXT-REF-123",
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
    "tenant_id, product_skus_override, expected_success, expected_message",
    [
        (
            # tenant_id
            "tenant_123",
            # Items Override (Original valid case)
            BASE_ORDER_INPUT["product_skus"],
            # expected_success
            True,
            # expected_message
            "Order successfully created.",
        ),
        (
            "tenant_123",
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
        ),
        (
            "tenant_123",
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
    tenant_id,
    product_skus_override,
    expected_success,
    expected_message,
):

    # Use deepcopy to avoid modifying the global BASE_ORDER_INPUT across tests
    input_data = copy.deepcopy(BASE_ORDER_INPUT)
    
    # Override the specific part that changes
    input_data["product_skus"] = product_skus_override

    access_control_mock = fake_access_control()
    
    
    # Create the access control instance
    access_control = access_control_mock.create_access_control(tenant_id)
    # The user context mock needs to match the tenant_id being tested
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, tenant_id)

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
