import pytest, copy
import graphene
from graphene.test import Client
from unittest.mock import MagicMock, PropertyMock
from ddd.order_management.application import commands, handlers, dtos, ports
from ddd.order_management.domain import enums
from ddd.order_management.entrypoints.graphql.mutations.confirm_shipment_mutation import ConfirmShipmentMutation 

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
        # Update this to use the new mutation class
        confirm_shipment = ConfirmShipmentMutation.Field() 
    
    # 2. Define a DUMMY Query class to satisfy the Client's requirement
    class DummyQuery(graphene.ObjectType):
        dummy = graphene.Boolean(default_value=True)
        
    # 3. Pass both the Query and Mutation container classes to the schema
    schema = graphene.Schema(query=DummyQuery, mutation=RootTestMutation)
    client = Client(schema)

    # Mock the internal infrastructure calls within the resolver function 
    # to return a controlled user_ctx for predictable tests.
    mocker.patch(
        "ddd.order_management.entrypoints.graphql.common.get_tenant_id",
        return_value="tenant_123"
    )
    # Mock the actual access control service call within the infrastructure
    mocker.patch(
        fake_get_user_context,
        return_value=user_context_tenant1_vendor_all_perms # Use our seeded context
    )
    
    
    return client


@pytest.mark.django_db # boto3 can ignore so we can use for AWS too
@pytest.mark.parametrize(
    "target_order_id, target_shipment_id, expected_success, expected_message",
    [
        (
            "ORD-CONFIRMED_W_PENDING-1",
            "SH-PENDING-2",
            # expected_success
            True,
            # expected_message
            "Order ORD-CONFIRMED_W_PENDING-1 w Shipment Id SH-PENDING-2 successfully confirmed."
        ),
        (
            "ORD-CONFIRMED_W_SHIPPED-1",
            "SH-SHIPPED-CONFIRMED-1",
            # expected_success
            False,
            # expected_message
            "Only pending shipment can be confirm"
        ),
    ]
)
def test_graphql_endpoint_confirm_shipment_successfully_e2e(
    fake_jwt_valid_token,
    graphene_client, 
    target_order_id, target_shipment_id,
    expected_success, expected_message,
    test_constants):
    """
    Test the GraphQL API using the Graphene test client. 
    This hits the resolver logic which uses the real message bus/handler 
    (which is mocked in the fixture) but has the UserContext injected via the mocked access control layers 
    in the fixture setup.
    """
    
    TENANT1 = test_constants.get("tenant1")
    VENDOR1 = test_constants.get("vendor1")

    # Create a mock object that looks like a Django request object for context passing
    mock_context = MagicMock()
    # Ensure the 'META' attribute behaves like a dictionary
    type(mock_context).META = PropertyMock(return_value={
        "HTTP_AUTHORIZATION": f"Bearer {fake_jwt_valid_token}"
    })


 # The GraphQL mutation query updated for ConfirmShipment
    query = """
            mutation ConfirmShipment($input: ConfirmShipmentMutationInput!) {
                confirmShipment(input: $input) {
                    result {
                        success
                        message
                    }
                }
            }
        """
    
    # The variables matching the Graphene input types
    variables = {
        "input": {
            "orderId": target_order_id,
            "shipmentId": target_shipment_id
        }
    }
    
    # Execute the GraphQL query
    response = graphene_client.execute(query, variables=variables, context=mock_context)

    # --- Assertions on the GraphQL Response ---
    assert response.get('errors') is None
    data = response['data']['confirmShipment']['result']
    assert data['success'] is expected_success
    # Update expected message to match the handler's output message format
    assert data['message'] == expected_message