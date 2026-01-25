import requests
import pytest

@pytest.mark.django_db
def test_graphql_add_order_via_http_e2e(api_gateway_url, live_keycloak_token):
    """
    Full E2E: Network -> API Gateway -> Lambda -> DynamoDB/Django.
    """
    
    # 1. Define the Input (The GraphQL Mutation + Variables)
    graphql_payload = {
        "query": """
            mutation AddOrder($input: AddOrderMutationInput!) {
                addOrder(input: $input) {
                    result { success message }
                }
            }
        """,
        "variables": {
            "input": {
                "tenantId": "tenant_123",
                "externalRef": "HTTP-E2E-TEST-999",
                "customerDetails": {
                    "name": "E2E User",
                    "email": "e2e@sfayn.com",
                    "customerId": "CUST-E2E"
                },
                "productSkus": [
                    {
                        "productSku": "SKU-A",
                        "productName": "E2E Item",
                        "orderQuantity": 1,
                        "vendorId": "VEND-1",
                        "package": {"weightKg": "1.0"},
                        "productPrice": {"amount": "15.0", "currency": "USD"}
                    }
                ]
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
        api_gateway_url, 
        json=graphql_payload, 
        headers=headers
    )

    # 4. Assertions
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data.get("errors") is None
    
    result = response_data["data"]["addOrder"]["result"]
    assert result["success"] is True
    assert "successfully" in result["message"]
