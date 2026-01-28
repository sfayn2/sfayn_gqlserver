import requests
import pytest

@pytest.mark.django_db
@pytest.mark.parametrize(
    "target_order_id, expected_success, expected_message",
    [
        (
            "ORD-CONFIRMED_W_CONFIRMED-1",
            # expected_success
            True,
            # expected_message
            "Order ORD-CONFIRMED_W_CONFIRMED-1 successfully canceled."
        ),
        (
            "ORD-CONFIRMED_W_PENDING-1",
            # expected_success
            True,
            # expected_message
            "Order ORD-CONFIRMED_W_PENDING-1 successfully canceled."
        ),
        (
            "ORD-CONFIRMED_W_SHIPPED-1",
            # expected_success
            False,
            # expected_message
            "Order in ORD-CONFIRMED_W_SHIPPED-1 cannot be canceled."
        ),
        (
            "ORD-CONFIRMED_W_DELIVERED-1",
            # expected_success
            False,
            # expected_message
            "Order in ORD-CONFIRMED_W_DELIVERED-1 cannot be canceled."
        ),
        (
            "ORD-ALREADY-COMPLETED-1",
            # expected_success
            False,
            # expected_message
            "Order in ORD-ALREADY-COMPLETED-1 cannot be canceled."
        ),
    ]
)
def test_mark_as_completed_full_e2e(
    api_gateway_url_graphql_api, 
    live_keycloak_token,
    target_order_id,
    expected_success,
    expected_message,
    test_constants
):
    """
    Full E2E: Network -> API Gateway -> Lambda -> DynamoDB/Django.
    """

    TENANT1 = test_constants.get("tenant1")
    VENDOR1 = test_constants.get("vendor1")
    
    # 1. Define the Input (The GraphQL Mutation + Variables)
    graphql_payload = {
        "query": """
            mutation CancelOrder($input: CancelOrderMutationInput!) {
                cancelOrder(input: $input) {
                    result {
                        success
                        message
                    }
                }
            }
        """,
        "variables": {
            "input": {
                "tenantId": TENANT1,
                "orderId": target_order_id,
            }
        }
    }


    # 2. Define Headers (Including the JWT)
    headers = {
        "Authorization": f"Bearer {live_keycloak_token}",
        "Content-Type": "application/json"
    }

    # 3. The Action: Send the physical POST request
    response = requests.post(
        api_gateway_url_graphql_api, 
        json=graphql_payload, 
        headers=headers,
    )

    response_data = response.json()

    # 4. Assertions
    assert response.status_code == 200
    
    assert response_data.get("errors") is None

    result = response_data['data']['cancelOrder']['result']
    assert result['success'] is expected_success
    assert result['message'] == expected_message

