import requests
import pytest

@pytest.mark.django_db
def test_add_shipment_full_e2e(api_gateway_url_graphql_api, live_keycloak_token, test_constants):
    """
    Full E2E: Network -> API Gateway -> Lambda -> DynamoDB/Django.
    """
    target_order_id = "ORD-CONFIRMED-1"
    TENANT1 = test_constants.get("tenant1")
    VENDOR1 = test_constants.get("vendor1")

    
    # 1. Define the Input (The GraphQL Mutation + Variables)
    graphql_payload = {
        "query": """
            mutation AddShipment($input: AddShipmentMutationInput!) {
                addShipment(input: $input) {
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
                "shipmentMode": "dropoff",
                "shipmentProvider": "FEDEX",
                "instructions": "Leave at the front door",
                
                # Package details (optional fields set here)
                "packageWeightKg": "2.5", 
                "packageLengthCm": "30",
                "packageWidthCm": "20",
                "packageHeightCm": "10",

                # Shipment Address (required)
                "shipmentAddress": {
                    "line1": "123 Main St",
                    "city": "Anytown",
                    "country": "USA",
                    "postal": "90210"
                },
                
                # Shipment Items (required list)
                "shipmentItems": [
                    {
                        "productSku": "SKU-A",
                        "quantity": 1,
                        "vendorId": VENDOR1
                    },
                    {
                        "productSku": "SKU-B",
                        "quantity": 1,
                        "vendorId": VENDOR1
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
        api_gateway_url_graphql_api, 
        json=graphql_payload, 
        headers=headers,
    )

    response_data = response.json()

    # 4. Assertions
    assert response.status_code == 200
    
    assert response_data.get("errors") is None

    # Check the data returned matches the seeded data
    data = response_data['data']['addShipment']['result']
    assert data['success'] == True
    assert data['message'] == f"Order {target_order_id} successfully add new shipment."
