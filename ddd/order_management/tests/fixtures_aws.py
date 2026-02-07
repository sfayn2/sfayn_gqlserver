import pytest, boto3, os, time, requests
from unittest.mock import MagicMock, PropertyMock
from decimal import Decimal 
from .fixtures import *
from .data import *



@pytest.fixture()
def api_gateway_url_graphql_api():
    """Dynamically discover the LocalStack API Gateway URL by API name."""

    endpoint_url="http://localhost:4566"

    # 1. Connect to LocalStack APIGateway
    client = boto3.client(
        "apigateway"
    )

    # 2. Get all REST APIs and find yours by name
    # Ensure this matches 'name' in your aws_api_gateway_rest_api terraform resource
    target_api_name = "tntoms-tst-api" 
    
    apis = client.get_rest_apis()
    print("APIS FOUND:", apis)
    api_id = next(
        (item["id"] for item in apis["items"] if item["name"] == target_api_name), 
        None
    )

    if not api_id:
        # Debugging tip: Print what WAS found if it fails
        found_names = [item["name"] for item in apis["items"]]
        raise Exception(
            f"Could not find API '{target_api_name}'. Found: {found_names}. "
            "Is your Terraform applied?"
        )

    # 3. Construct the URL
    stage = "tst"
    time.sleep(3) # Wait for eventual consistency for unknown reasons, it needs to have a breathing time
    return f"{endpoint_url}/_aws/execute-api/{api_id}/{stage}/graphql"


#@pytest.fixture(scope="session")
@pytest.fixture
def live_keycloak_token(fake_jwt_valid_token):
    """Grabs a real token from a running Keycloak instance."""
    # 2. Define Headers (Including the JWT)
    if os.getenv("SKIP_JWT_VERIFY") == "true":
        print("⚠️ SKIP_JWT_VERIFY is true, using fake token.", fake_jwt_valid_token)
        return fake_jwt_valid_token
    else:
        url = "http://localhost:8080/realms/TenantOMSAPI-Realm/protocol/openid-connect/token"
        data = {
            "client_id": "TenantOMSAPI-Client",
            "client_secret": os.getenv("KC_CLIENT_SECRET"),
            "grant_type": "password",
            "username": "pao",
            "password": os.getenv("KC_PWD")
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        time.sleep(2) # Wait for eventual consistency for unknown reasons, it needs to have a breathing time

        return response.json()["access_token"]


@pytest.fixture
def fake_get_user_context():    
    return 'ddd.order_management.infrastructure.access_control1.DynamodbAccessControl1.get_user_context'

@pytest.fixture(scope="session", autouse=True)
def seeded_all():
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # 1. Pre-Wipe the Table
    scan = table.scan(ProjectionExpression='pk, sk')
    with table.batch_writer() as batch:
        for each in scan.get('Items', []):
            batch.delete_item(Key={'pk': each['pk'], 'sk': each['sk']})

    # 2. Batch Seed using Named Unpacking
    with table.batch_writer() as batch:
        
        # 1. Tenant Configs
        for tc in TENANT_CONFIG_SEEDS:
            t_id, configs, dt = tc
            batch.put_item(Item={
                "pk": f"TENANT#{t_id}", 
                "sk": "CONFIG#TENANT",
                "configs": configs, 
                "last_update_dt": dt.isoformat() if hasattr(dt, 'isoformat') else dt
            })

        # 2. SaaS Configs
        for sas in SAAS_CONFIG_SEEDS:
            t_id, configs, dt = sas
            batch.put_item(Item={
                "pk": f"TENANT#{t_id}", 
                "sk": "CONFIG#SAAS",
                "configs": configs, 
                "last_update_dt": dt.isoformat() if hasattr(dt, 'isoformat') else dt
            })

        # 3. User Authorizations
        for us in USER_SEEDS:
            t_id, perm, scope, active = us
            batch.put_item(Item={
                "pk": f"TENANT#{t_id}", 
                "sk": f"AUTH#USER#{perm}",
                "scope": scope,
                "is_active": active
            })

        # 4. Orders
        for os_data in ORDER_SEEDS:
            (oid, tid, ver, ref, stat, cid, cname, cmail, pstat, curr, cdt, mdt) = os_data
            batch.put_item(Item={
                "pk": f"TENANT#{tid}", 
                "sk": f"ORDER#{oid}",
                "order_id": oid, "tenant_id": tid, "version": ver,
                "external_ref": ref, "order_status": stat,
                "customer_id": cid, "customer_name": cname, "customer_email": cmail,
                "payment_status": pstat, "currency": curr,
                "date_created": cdt.isoformat(), "date_modified": mdt.isoformat(),
                "entity_type": "ORDER"
            })

        # 5. Order Lines
        for ol in ORDER_LINE_SEEDS:
            oid, sku, name, price, curr, qty, vid, weight = ol
            batch.put_item(Item={
                "pk": f"ORDER#{oid}", 
                "sk": f"LINE#{sku}",
                "product_sku": sku, "product_name": name,
                "product_price": Decimal(str(price)),
                "product_currency": curr, "order_quantity": qty,
                "vendor_id": vid, "package_weight_kg": Decimal(str(weight)),
                "entity_type": "LINE_ITEM"
            })

        # 6. Shipments
        for sh in SHIPMENT_SEEDS:
            (sid, oid, l1, l2, city, post, country, state, prov, track, amt, curr, stat, tenant_id) = sh
            batch.put_item(Item={
                "pk": f"ORDER#{oid}", 
                "sk": f"SHIPMENT#{sid}",
                "order_id": oid,
                "tenant_id": tenant_id,
                "line1": l1, "line2": l2, "city": city, "postal": post,
                "country": country, "state": state, "provider": prov,
                "tracking_reference": track, "amount": Decimal(str(amt)),
                "currency": curr, "status": stat,
                "entity_type": "SHIPMENT"
            })

        # 7. Shipment Items
        for shi in SHIPMENT_ITEM_SEEDS:
            item_id, order_id, ship_id, sku, qty = shi
            batch.put_item(Item={
                "pk": f"ORDER#{order_id}", 
                "sk": f"SHIPMENT#{ship_id}#ITEM#{item_id}#SKU#{sku}",
                "shipment_id": ship_id,
                "shipment_item_id": item_id,
                "line_item_sku": sku, 
                "quantity": qty,
                "entity_type": "SHIPMENT_ITEM"
            })

        # 8. User Action Logs
        for ual in USER_ACTION_SEEDS:
            oid, act, by, inp, ts = ual
            batch.put_item(Item={
                "pk": f"ORDER#{oid}", 
                "sk": f"LOG#{ts.isoformat()}#{act}",
                "action": act, "performed_by": by, "user_input": inp
            })
            
    print("✅ DynamoDB Seeding Completed Successfully.")

@pytest.fixture
def mock_context_w_auth_header_token(fake_jwt_valid_token):
    # Satisfies CASE 2: Lambda (isinstance(ctx, dict) and "request_event" in ctx)
    # Note: To pass isinstance(mock_context, dict), you must use a different approach:
    mock_context = {
        "request_event": {
            "headers": {"Authorization": f"Bearer {fake_jwt_valid_token}"}
        }
    }
    return mock_context


def post_webhook_request(path_prefix: str, identifier: str, data: dict, api_name: str = "tntoms-tst-api"):
    """
    Common utility to post webhooks to LocalStack API Gateway.
    """
    endpoint_url = "http://localhost:4566"
    stage = "tst"
    
    # 1. Resolve API ID
    client = boto3.client("apigateway")
    apis = client.get_rest_apis()
    api_id = next(
        (item["id"] for item in apis["items"] if item["name"] == api_name), 
        None
    )

    if not api_id:
        raise Exception(f"API '{api_name}' not found. Verify LocalStack state.")

    # 2. Construct URL dynamically
    # Matches: /webhook/shipment-tracker/saas_123 OR /webhook/add-order/tenant_abc
    url = f"{endpoint_url}/_aws/execute-api/{api_id}/{stage}/webhook/{path_prefix}/{identifier}"

    # 3. Security Headers
    headers = {
        "x-wss-signature": "d1f4101d6368bc38c2075bc4893293c71c61e0250c7eb8fd9c44d70a9c59906c",
        "x-wss-timestamp": str(int(time.time())),
        "Content-Type": "application/json"
    }

    # 4. Execute Request
    return requests.post(url, json=data, headers=headers)


@pytest.fixture
def generic_request_post_shipment_tracker_webhook(tracker_data_dict, test_constants):

    """Specific fixture for SaaS-based shipment tracker."""
    return post_webhook_request(
        path_prefix="shipment-tracker",
        identifier=test_constants.get("saas1"),
        data=tracker_data_dict
    )

@pytest.fixture
def generic_request_post_shipment_tracker_webhook_tenant(tracker_data_dict, test_constants):

    """Specific fixture for SaaS-based shipment tracker."""
    return post_webhook_request(
        path_prefix="shipment-tracker",
        identifier=test_constants.get("tenant1"),
        data=tracker_data_dict
    )


    ## Get the API ID dynamically from the environment
    #SAAS_ID = test_constants.get("saas1")

    #endpoint_url = "http://localhost:4566"

    ## 1. Connect to LocalStack APIGateway
    #client = boto3.client(
    #    "apigateway"
    #)

    ## 2. Get all REST APIs and find yours by name
    ## Ensure this matches 'name' in your aws_api_gateway_rest_api terraform resource
    #target_api_name = "tntoms-tst-api" 
    
    #apis = client.get_rest_apis()
    #print("APIS FOUND:", apis)
    #api_id = next(
    #    (item["id"] for item in apis["items"] if item["name"] == target_api_name), 
    #    None
    #)

    #if not api_id:
    #    # Debugging tip: Print what WAS found if it fails
    #    found_names = [item["name"] for item in apis["items"]]
    #    raise Exception(
    #        f"Could not find API '{target_api_name}'. Found: {found_names}. "
    #        "Is your Terraform applied?"
    #    )

    ## 3. Construct the URL
    #stage = "tst"

    ## AWS API Gateway Endpoint Format for LocalStack
    ##url = f"{endpoint_url}/restapis/{api_id}/{stage}/_user_request_/webhook/shipment-tracker/{SAAS_ID}"
    #url = f"{endpoint_url}/_aws/execute-api/{api_id}/{stage}/webhook/shipment-tracker/{SAAS_ID}"

    ## Standard HTTP headers (no 'HTTP_' prefix)
    #headers = {
    #    "x-wss-signature": "d1f4101d6368bc38c2075bc4893293c71c61e0250c7eb8fd9c44d70a9c59906c",
    #    "x-wss-timestamp": str(int(time.time())),
    #    "Content-Type": "application/json"
    #}

    ## Real network POST request
    #response = requests.post(
    #    url,
    #    data=json.dumps(tracker_data_dict),
    #    headers=headers
    #)

    #return response