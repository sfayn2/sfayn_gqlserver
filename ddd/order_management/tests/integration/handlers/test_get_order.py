import pytest
import json
import traceback
import graphene
from unittest.mock import MagicMock
from datetime import datetime, timezone
from decimal import Decimal
from graphene.test import Client
from ddd.order_management.application import queries, dtos
from ddd.order_management.domain import exceptions, enums
# Import the code under test (GetOrderQuery class)
from ddd.order_management.presentation.graphql.queries.get_order_query import GetOrderQuery
# Import the handler function to test handler logic directly
from ddd.order_management.application.handlers import handle_get_order


@pytest.fixture
def graphene_client(mocker, user_context_tenant1_vendor_all_perms):
    """
    Fixture to create a Graphene client configured for testing the GraphQL endpoint.
    
    We need to mock the access_control and common.get_token_from_context 
    parts of the Graphene resolver logic slightly to control the exact 
    user context passed to the handler, since we are not mocking the handler itself.
    """
    schema = graphene.Schema(query=GetOrderQuery)
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

@pytest.fixture
def user_context_tenant1_vendor_all_perms(test_constants) -> dtos.UserContextDTO:
    """Provides a valid UserContextDTO for TENANT1 with all vendor permissions."""
    TENANT1 = test_constants.get("tenant1")
    USER1 = test_constants.get("user1")
    return dtos.UserContextDTO(
        sub=USER1,
        token_type="Bearer",
        tenant_id=TENANT1,
        roles=["vendor"]
    )


# =====================================================================
# Test the Application Handler Logic directly (Unit/Integration Test)
# =====================================================================
@pytest.mark.django_db
def test_handler_can_retrieve_existing_order(
    fake_access_control,
    fake_exception_handler,
    fake_user_action_service,
    fake_jwt_valid_token,
    fake_uow,
    test_constants):
    """Test that the handle_get_order function returns the correct order DTO when data exists."""
    
    # We use uow_with_seeded_data fixture (assumed to be in conftest.py) 
    # which connects to a DB and runs seeds.
    target_order_id = "ORD-CONFIRMED-1"
    query = queries.GetOrderQuery(order_id=target_order_id)
    TENANT1 = test_constants.get("tenant1")


    # Configure access control mock based on test case requirements
    access_control_service = fake_access_control()
        
    access_control = access_control_service.create_access_control(TENANT1) 
    user_ctx = access_control.get_user_context(fake_jwt_valid_token, TENANT1)

    
    # Execute the handler function using the real UoW (which talks to the DB)
    order_dto = handle_get_order(
        query=query, 
        access_control=access_control, # Using the real access control infra
        user_ctx=user_ctx,
        uow=fake_uow,
        exception_handler=fake_exception_handler,
        user_action_service=fake_user_action_service
    )

    #assert isinstance(order_dto, dtos.OrderResponseDTO)
    assert order_dto.order_id == target_order_id
    assert order_dto.tenant_id == TENANT1
    assert order_dto.order_status == enums.OrderStatus.CONFIRMED



# =====================================================================
# Test the GraphQL Endpoint using the Graphene Client (E2E Test)
# =====================================================================
@pytest.mark.django_db
def test_graphql_endpoint_retrieves_order_successfully(
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

    
    # GraphQL query string expanded to include ALL fields
    query = f"""
        query {{
          getOrderByOrderId(orderId: "{target_order_id}") {{
            orderId,
            orderStatus,
            tenantId,
            currency,
            dateModified,
            dateCreated,
            customerDetails {{
              customerId,
              name,
              email
            }},
            lineItems {{
              productSku,
              productName,
              orderQuantity,
              vendorId,
              productPrice {{
                amount,
                currency
              }},
              package {{
                weight
              }}
            }}
          }}
        }}
    """
    
    response = graphene_client.execute(query, context=mock_context)

    # Check that no errors occurred in the GraphQL execution
    assert response.get('errors') is None
    # Check the data returned matches the seeded data
    data = response['data']['getOrderByOrderId']
    # --- Start Assertions for all fields ---
    assert data['orderId'] == target_order_id
    # Assuming enums.OrderStatus.CONFIRMED.value is 'CONFIRMED'
    assert data['orderStatus'] == 'CONFIRMED' 
    assert data['tenantId'] == 'tenant_123'
    assert data['currency'] == 'SGD'


    # Get the current time truncated to the minute, in UTC
    current_utc_time = datetime.now(timezone.utc)
    
    # 1. Format for dateModified (uses 'T' separator)
    # e.g., '2025-12-13T14:26'
    prefix_date_modified = current_utc_time.strftime('%Y-%m-%dT%H:%M')

    # 2. Format for dateCreated (uses ' ' space separator)
    # e.g., '2025-12-13 14:26'
    prefix_date_created = current_utc_time.strftime('%Y-%m-%d %H:%M')
    
    # Asserts that the dateModified string starts with the YYYY-MM-DDTHH:MM
    assert data['dateModified'].startswith(prefix_date_modified)

    # Asserts that the dateCreated string starts with the YYYY-MM-DD HH:MM (using a space)
    assert data['dateCreated'].startswith(prefix_date_created)


    
    # Assert nested Customer Details
    assert data['customerDetails']['customerId'] == 'customer id here'
    assert data['customerDetails']['name'].strip() == 'customer name'
    assert data['customerDetails']['email'].strip() == 'customer email'
    
    # Assert Line Items (The response has 2 items)
    assert len(data['lineItems']) == 2
    
    # Assert details for the first line item
    item1 = data['lineItems'][0]
    assert item1['productSku'] == 'SKU-A'
    assert item1['productName'] == 'my product'
    assert item1['orderQuantity'] == 2
    assert item1['vendorId'] == 'vendor-1'
    assert item1['productPrice']['amount'] == '1.12' # Graphene Decimal returns as string
    assert item1['productPrice']['currency'] == 'SGD'
    assert item1['package']['weight'] is None
    
    # Assert details for the second line item
    item2 = data['lineItems'][1]
    assert item2['productSku'] == 'SKU-B'
    assert item2['productName'] == 'my product'
    assert item2['orderQuantity'] == 2
    assert item2['vendorId'] == 'vendor-1'
    assert item2['productPrice']['amount'] == '1.12'
    assert item2['productPrice']['currency'] == 'SGD'
    assert item2['package']['weight'] is None

   
@pytest.mark.django_db
def test_graphql_endpoint_returns_null_for_missing_order(
    fake_jwt_valid_token,
    graphene_client, mocker):
    """
    Test the GraphQL API behavior when the underlying handler raises a NotFound exception.
    Graphene resolvers often return `None` (null in JSON) if an expected object isn't found, 
    rather than causing a top-level GraphQL error, depending on your schema definition.
    """
    invalid_order_id = "ORD-DOES-NOT-EXIST"

    # Create a mock object that looks like a Django request object
    mock_context = MagicMock()
    mock_context.META = {
        "HTTP_AUTHORIZATION": f"Bearer {fake_jwt_valid_token}"
    }


    query = f"""
        query {{
          getOrderByOrderId(orderId: "{invalid_order_id}") {{
            orderId
          }}
        }}
    """

    response = graphene_client.execute(query, context=mock_context)

    # The data field for the query should be null when NotFound is raised
    assert response['data']['getOrderByOrderId'] is None
    # Depending on how your exception handler is configured, you might also check errors:
    # assert response.get('errors') is not None 

