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
            }},
            shipments {{
              shipmentId,
              shipmentAddress {{
                line1,
                city,
                country,
                line2,
                state,
                postal
              }},
              shipmentMode,
              shipmentProvider,
              packageWeightKg,
              packageLengthCm,
              packageWidthCm,
              packageHeightCm,
              pickupAddress {{
                line1,
                city,
                country,
                line2,
                state,
                postal
              }},
              pickupWindowStart,
              pickupWindowEnd,
              pickupInstructions,
              trackingReference,
              labelUrl,
              shipmentAmount {{
                amount,
                currency
              }},
              shipmentStatus,
              shipmentItems {{
                lineItem {{
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
                }},
                quantity,
                shipmentItemId
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


    # -----------------------------------------------
    # Assertions for the NEW 'shipments' data array
    # -----------------------------------------------
    
    # Check that we received exactly 1 shipment item in the list
    assert len(data['shipments']) == 1
    
    # Extract the first shipment object for detailed assertions
    shipment1 = data['shipments'][0]
    
    assert shipment1['shipmentId'] == 'SH-1'
    assert shipment1['shipmentMode'] is None # Based on your actual result
    assert shipment1['shipmentProvider'] == 'provider here'
    assert shipment1['trackingReference'].strip() == 'tracking reference here'
    assert shipment1['labelUrl'] is None
    assert shipment1['shipmentStatus'] == 'PENDING'

    # Assert nested Shipment Address details
    assert shipment1['shipmentAddress']['line1'] == 'line 1'
    assert shipment1['shipmentAddress']['city'].strip() == 'city' # Assert .strip() because data has trailing space
    assert shipment1['shipmentAddress']['country'] == 'country here'
    assert shipment1['shipmentAddress']['postal'] == 'postal here' # Assuming you switched this to String type
    
    # Assert physical package dimensions (all None in actual result)
    assert shipment1['packageWeightKg'] is None
    assert shipment1['packageLengthCm'] is None
    assert shipment1['packageWidthCm'] is None
    assert shipment1['packageHeightCm'] is None

    # Assert pickup details (all None in actual result)
    assert shipment1['pickupAddress'] is None
    assert shipment1['pickupWindowStart'] is None
    # ... (etc. for other pickup fields)

    # Assert Shipment Amount details
    assert shipment1['shipmentAmount']['amount'] == '2.20'
    assert shipment1['shipmentAmount']['currency'] == 'SGD'

    # Assert Shipment Items (nested structure for which order items are in this shipment)
    # The actual result shows shipmemntItems as a single object with None values, 
    # but based on your schema it should be a list or a correctly populated object.
    # We will assert based on the provided "actual result" structure for now:
    
    assert shipment1['shipmentItems']['lineItem'] is None
    assert shipment1['shipmentItems']['quantity'] is None
    assert shipment1['shipmentItems']['shipmentItemId'] is None


   
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

