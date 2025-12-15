import pytest, copy
import graphene
from graphene.test import Client
from unittest.mock import MagicMock
from ddd.order_management.application import commands, handlers, dtos, ports
from ddd.order_management.domain import enums
from order_management import models as django_snapshots
from ddd.order_management.presentation.graphql.mutations.cancel_order_mutation import CancelOrderMutation

# Use global constants defined in conftest.py (assumed to be in scope)



# =====================================================================
# Test the GraphQL Endpoint using the Graphene Client (E2E Test)
# =====================================================================

@pytest.fixture
def graphene_client(mocker, user_context_tenant1_vendor_all_perms):
    """
    Fixture to create a Graphene client configured for testing the GraphQL endpoint.
    
    We need to mock the access_control and common.get_token_from_context 
    parts of the Graphene resolver logic slightly to control the exact 
    user context passed to the handler, since we are not mocking the handler itself.
    """

    # 1. Define a local temporary Mutation container class
    class RootTestMutation(graphene.ObjectType):
        cancel_order = CancelOrderMutation.Field()
    
    # 2. Define a DUMMY Query class to satisfy the Client's requirement
    class DummyQuery(graphene.ObjectType):
        dummy = graphene.Boolean(default_value=True)
        
    # 3. Pass both the Query and Mutation container classes to the schema
    schema = graphene.Schema(query=DummyQuery, mutation=RootTestMutation)
    client = Client(schema)

    # Mock the internal infrastructure calls within the resolver function 
    # to return a controlled user_ctx for predictable tests.
    mocker.patch(
        "ddd.order_management.presentation.graphql.common.get_tenant_id",
        return_value="tenant_123"
    )
    mocker.patch(
        'ddd.order_management.infrastructure.access_control1.AccessControl1.get_user_context',
        return_value=user_context_tenant1_vendor_all_perms # Use our seeded context
    )
    
    return client



@pytest.mark.django_db
def test_graphql_endpoint_cancels_order_successfully_e2e(
    fake_jwt_valid_token,
    graphene_client, 
    test_constants):
    """
    Test the GraphQL API using the Graphene test client. 
    This hits the resolver logic which uses the real message bus/handler 
    but has the UserContext injected via the mocked access control layers 
    in the fixture setup.
    """
    
    target_order_id = "ORD-CONFIRMED-1"
    TENANT1 = test_constants.get("tenant1")

    # Create a mock object that looks like a Django request object
    mock_context = MagicMock()
    mock_context.META = {
        "HTTP_AUTHORIZATION": f"Bearer {fake_jwt_valid_token}"
    }

    query = """
            mutation CancelOrder($orderId: String!) {
                cancelOrder(input: { orderId: $orderId }) {
                    result {
                        success
                        message
                    }
                }
            }
        """
    variables = {"orderId": target_order_id}
    
    # Execute the GraphQL query
    # We use a mock 'info' context here if needed, but the fixtures handle the common calls
    response = graphene_client.execute(query, variables=variables, context=mock_context)

    # Check that no errors occurred in the GraphQL execution
    assert response.get('errors') is None
    # Check the data returned matches the seeded data
    data = response['data']['cancelOrder']['result']
    assert data['success'] == True
    assert data['message'] == 'Order ORD-CONFIRMED-1 successfully canceled.'