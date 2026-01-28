import requests
import pytest

@pytest.mark.django_db
@pytest.mark.parametrize(
    "target_order_id, expected_success, expected_message",
    [
        (
            "ORD-READY-TO-COMPLETE-PAID-1",
            # expected_success
            True,
            # expected_message
            "Order ORD-READY-TO-COMPLETE-PAID-1 successfully mark as completed."
        ),
        (
            "ORD-CONFIRMED_W_SHIPPED-1",
            # expected_success
            False,
            # expected_message
            "Only delivered order can mark as completed."
        ),
        (
            "ORD-CONFIRMED_W_PENDING-1",
            # expected_success
            False,
            # expected_message
            "Only delivered order can mark as completed."
        ),
        (
            "ORD-CONFIRMED_W_CONFIRMED-1",
            # expected_success
            False,
            # expected_message
            "Only delivered order can mark as completed."
        ),
        (
            "ORD-READY-TO-COMPLETE-UNPAID-1",
            # expected_success
            False,
            # expected_message
            "Cannot mark as completed with outstanding payments."
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
            mutation MarkAsCompleted($input: MarkAsCompletedMutationInput!) {
                markAsCompleted(input: $input) {
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

    result = response_data['data']['markAsCompleted']['result']
    assert result['success'] is expected_success
    assert result['message'] == expected_message

