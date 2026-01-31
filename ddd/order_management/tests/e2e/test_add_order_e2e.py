import pytest, copy, os
import graphene
from graphene.test import Client
from unittest.mock import MagicMock, PropertyMock
from ddd.order_management.application import commands, handlers, dtos, ports
from ddd.order_management.domain import enums
from ddd.order_management.entrypoints.graphql.mutations.add_order_mutation import AddOrderMutation
from ddd.order_management.bootstrap import enums as infra_enums

# Use global constants defined in conftest.py (assumed to be in scope)

# =====================================================================
# Test the GraphQL Endpoint using the Graphene Client (E2E Test)
# =====================================================================

@pytest.fixture
def graphene_client(mocker, user_context_tenant1_vendor_all_perms, fake_get_user_context):
    """
    Fixture to create a Graphene client configured for testing the GraphQL endpoint.
    
    We need to mock the access_control and common.get_token_from_context 
    parts of the Graphene resolver logic slightly to control the exact 
    user context passed to the handler, since we are not mocking the handler itself.
    """

    # 1. Define a local temporary Mutation container class
    class RootTestMutation(graphene.ObjectType):
        add_order = AddOrderMutation.Field()
    
    # 2. Define a DUMMY Query class to satisfy the Client's requirement
    class DummyQuery(graphene.ObjectType):
        dummy = graphene.Boolean(default_value=True)
        
    # 3. Pass both the Query and Mutation container classes to the schema
    schema = graphene.Schema(query=DummyQuery, mutation=RootTestMutation)
    client = Client(schema)

    # Mock the internal infrastructure calls within the resolver function 
    # to return a controlled user_ctx for predictable tests.
    #mocker.patch(
    #    "ddd.order_management.entrypoints.graphql.common.get_tenant_id",
    #    return_value="tenant_123"
    #)
    # Mock the actual access control service call within the infrastructure
    mocker.patch(
        fake_get_user_context,
        return_value=user_context_tenant1_vendor_all_perms # Use our seeded context
    )
    
    
    return client


@pytest.mark.django_db # boto3 can ignore so we can use for AWS too
def test_graphql_endpoint_add_order_successfully_e2e(
    fake_jwt_valid_token,
    graphene_client, 
    mock_context_w_auth_header_token,
    test_constants):
    """
    Test the GraphQL API using the Graphene test client. 
    This hits the resolver logic which uses the real message bus/handler 
    (which is mocked in the fixture) but has the UserContext injected via the mocked access control layers 
    in the fixture setup.
    """
    
    target_external_ref = "EXT-REF-12345"
    TENANT1 = test_constants.get("tenant1")

    #if os.getenv("ORDER_MANAGEMENT_INFRA_TYPE") == infra_enums.InfraType.ONPREM_DJANGO.value:
    #    # Satisfies CASE 1: Django Request

    #    # Create a mock object that looks like a Django request object for context passing
    #    mock_context = MagicMock()
    #    # Ensure the 'META' attribute behaves like a dictionary
    #    type(mock_context).META = PropertyMock(return_value={
    #        "HTTP_AUTHORIZATION": f"Bearer {fake_jwt_valid_token}"
    #    })
    #else:

    #    # Satisfies CASE 2: Lambda (isinstance(ctx, dict) and "request_event" in ctx)
    #    # Note: To pass isinstance(mock_context, dict), you must use a different approach:
    #    mock_context = {
    #        "request_event": {
    #            "headers": {"Authorization": f"Bearer {fake_jwt_valid_token}"}
    #        }
    #    }




    # Updated query string to match the `AddOrderMutation`'s input structure
    query = """
            mutation AddOrder($input: AddOrderMutationInput!) {
                addOrder(input: $input) {
                    result {
                        success
                        message
                    }
                }
            }
        """
    
    # Updated variables dictionary to match the `AddOrderMutation.Input` fields
    variables = {
        "input": {
            "tenantId": TENANT1,
            "externalRef": target_external_ref,
            "customerDetails": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "customerId": "CUST-ABC-123"
            },
            "productSkus": [
                {
                    "productSku": "SKU-PROD-A",
                    "productName": "Product A",
                    "orderQuantity": 2,
                    "vendorId": "VEND-1",
                    "package": {
                        "weightKg": "20"
                    },
                    "productPrice": {
                        "amount": "19.99",
                        "currency": "USD"
                    }
                },
                {
                    "productSku": "SKU-PROD-B",
                    "productName": "Product B",
                    "orderQuantity": 1,
                    "vendorId": "VEND-1",
                    "package": {
                        "weightKg": "20"
                    },
                    "productPrice": {
                        "amount": "50.00",
                        "currency": "USD"
                    }
                }
            ]
        }
    }
    
    # Execute the GraphQL query
    # We pass the mock_context to the client execution
    response = graphene_client.execute(query, variables=variables, context=mock_context_w_auth_header_token)

    # Check that no errors occurred in the GraphQL execution
    assert response.get('errors') is None
    # Check the data returned matches the seeded data
    data = response['data']['addOrder']['result']
    assert data['success'] == True
    assert data['message'].startswith('Order ORD')
    assert data['message'].endswith(' successfully created.')


