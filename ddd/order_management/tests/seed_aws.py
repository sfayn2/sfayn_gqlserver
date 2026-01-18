import pytest, json, jwt, os, boto3
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from decimal import Decimal
from ddd.order_management.domain import (
    models,
    repositories as domain_ports,
    services as domain_services,
    value_objects,
    exceptions,
    enums
)
from ddd.order_management.application import (
    dtos, 
)
from ddd.order_management.infrastructure import (
    event_bus, 
    repositories,
    access_control1,
    event_publishers,
    webhook_receiver,
    clocks,
    user_action_service,
    tenant_lookup_service,
    saas_lookup_service,
    shipping,
    exception_handler
)

# =================
# RSA key
# =========
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



# === Test Data ========
USER1 = "user-1"
USER2 = "user-2"
SAAS1 = "saas_123"
TENANT1 = "tenant_123"
TENANT2 = "tenant_456"
VENDOR1 = "vendor-1"
VENDOR2 = "vendor-2"

VENDOR_PERMISSIONS = [
    "add_order",
    "cancel_order",
    "add_shipment",
    "cancel_shipment",
    "confirm_shipment",
    "deliver_shipment",
    "mark_as_completed",
    "get_order",
    # Add more permissions here easily
]

# Generate the USER_SEEDS tuple using a generator expression
# Columns tenant_id, permission_codename, scope, is_active
USER_SEEDS = tuple(
    (TENANT1, permission, json.dumps({ "role": ["vendor"] }), True)
    for permission in VENDOR_PERMISSIONS
)
#USER_SEEDS = (
#    (TENANT1, "add_shipment", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "add_order", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "cancel_order", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "cancel_shipment", json.dumps({ "role": ["vendor"] }), True),
#)

# Columns order_id, tenant_id, version, external_ref, order_status, customer_id, customer_name, customer_email, payment_status, currency, date_created, date_modified
ORDER_SEEDS = (
    ("ORD-CONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)), 
    ("ORD-NOTCONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-DRAFT-1", TENANT1, 1, "external ref here", enums.OrderStatus.DRAFT.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_SHIPPED-1", TENANT1, 1, "external ref here", enums.OrderStatus.SHIPPED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_PENDING-1", TENANT1, 1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_CONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_DELIVERED-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-ALREADY-COMPLETED-1", TENANT1, 1, "external ref here", enums.OrderStatus.COMPLETED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-UNPAID-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-PAID-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
)

# Columns order_id, product_sku, product_name, product_price, product_currency, order_quantity, vendor_id, package_weight_kg
ORDER_LINE_SEEDS = (
    ("ORD-CONFIRMED-1", "SKU-A", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED-1", "SKU-B", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-NOTCONFIRMED-1", "SKU-NOTCONFIRMED", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_SHIPPED-1", "SKU-C", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_PENDING-1", "SKU-D", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_CONFIRMED-1", "SKU-E", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_DELIVERED-1", "SKU-F", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-1", "SKU-G", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-ALREADY-COMPLETED-1", "SKU-H", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-UNPAID-1", "SKU-I", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-PAID-1", "SKU-J", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
)

# Shipment
# Columns shipment_id, order_id, shipment_address_line1, shipment_address_line2, shipment_address_city, shipment_address_postal, shipment_address_country, shipment_address_state, shipment_provider, tracking_reference, shipment_amount, shipment_currency, shipment_status
SHIPMENT_SEEDS = (
    ("SH-1", "ORD-CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value),
    ("SH-SHIPPED-SHIPPED-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456789", Decimal("2.2"), "SGD", enums.ShipmentStatus.SHIPPED.value),
    ("SH-SHIPPED-SHIPPED-2", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456789", Decimal("2.2"), "SGD", enums.ShipmentStatus.SHIPPED.value),
    ("SH-SHIPPED-PENDING-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456789", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value),
    ("SH-SHIPPED-CONFIRMED-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456789", Decimal("2.2"), "SGD", enums.ShipmentStatus.CONFIRMED.value),
    ("SH-PENDING-2", "ORD-CONFIRMED_W_PENDING-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value),
    ("SH-CONFIRMED-2", "ORD-CONFIRMED_W_CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.CONFIRMED.value),
    ("SH-DELIVERED-2", "ORD-CONFIRMED_W_DELIVERED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-READY-TO-COMPLETE-1", "ORD-READY-TO-COMPLETE-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-ALREADY-COMPLETED-1", "ORD-ALREADY-COMPLETED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-READY-TO-COMPLETE-UNPAID-1", "ORD-READY-TO-COMPLETE-UNPAID-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-READY-TO-COMPLETE-PAID-1", "ORD-READY-TO-COMPLETE-PAID-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
)


# Shipment Item
# Columns shipment_item_id, order_id, shipment_id, line_item_id, quantity
SHIPMENT_ITEM_SEEDS = (
    ("SHI-1", "ORD-CONFIRMED-1", "SH-1", "SKU-A", 1, None, None),
    ("SHI-SHIPPED-1", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-SHIPPED-1", "SKU-C", 1),
    ("SHI-SHIPPED-2", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-PENDING-1", "SKU-C", 1),
    ("SHI-SHIPPED-3", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-CONFIRMED-1", "SKU-C", 1),
    ("SHI-SHIPPED-4", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-SHIPPED-2", "SKU-C", 1),
    ("SHI-PENDING-1", "ORD-CONFIRMED_W_PENDING-1", "SH-PENDING-2", "SKU-D", 1),
    ("SHI-CONFIRMED-1", "ORD-CONFIRMED_W_CONFIRMED-1", "SH-CONFIRMED-2", "SKU-E", 1),
    ("SHI-DELIVERED-1", "ORD-CONFIRMED_W_DELIVERED-1", "SH-DELIVERED-2", "SKU-F", 1),
    ("SHI-READY-TO-COMPLETE-1", "ORD-READY-TO-COMPLETE-1", "SH-READY-TO-COMPLETE-1", "SKU-G", 1),
    ("SHI-ALREADY-COMPLETED-1", "ORD-ALREADY-COMPLETED-1", "SH-SHIPPED_2", "SKU-H", 1),
    ("SHI-READY-TO-COMPLETE-UNPAID-1", "ORD-READY-TO-COMPLETE-UNPAID-1", "SH-READY-TO-COMPLETE-UNPAID-1", "SKU-I", 1),
    ("SHI-READY-TO-COMPLETE-PAID-1", "ORD-READY-TO-COMPLETE-PAID-1", "SH-READY-TO-COMPLETE-PAID-1", "SKU-J", 1),
)

# UserActionLog
# Columns order_id, action, performed_by, user_input, executed_at
USER_ACTION_SEEDS = (
    ("ORD-CONFIRMED-1", "add_order", USER1, json.dumps({}), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_SHIPPED-1", "cancel_order", USER1, json.dumps({}), datetime.now(timezone.utc)),
)

# TenantConfig
# Columns tenant_id, configs, last_update_dt
TENANT_CONFIG_SEEDS  = (
    (TENANT1, json.dumps({
        "restocking_fee_percent": 10,
        "max_refund_amount": 500.0,
    }), datetime.now(timezone.utc)),
)

# SaaSConfig
# Columns tenant_id, configs, last_update_dt
SAAS_CONFIG_SEEDS  = (
    (SAAS1, json.dumps({
        "idp": {},
        "webhooks": {
            "shipment_tracker": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
                "tracking_reference_jmespath": "tracking_number",
            },
            "add_order": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
            }
        },
        "create_shipment_api": {
            "provider": "wss",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
    (TENANT1, json.dumps({
        "idp": {
            "public_key": "http://localhost:8080/realms/ecommerce_realm/protocol/openid-connect/certs",
            "issuer": "http://localhost:8080/realms/ecommerce_realm",
            "audience": "AUD1",
            "algorithm": "RS256",
        },
        "webhooks": {
            "shipment_tracker": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
                "tracking_reference_jmespath": "result.tracking_code || data.tracking_code",
            },
            "add_order": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
            }
        },
        "create_shipment_api": {
            "provider": "wss",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
)

# === Test Data ========

@pytest.fixture(scope="session", autouse=True)
def test_constants():
    return {
        "saas1": SAAS1,
        "tenant1": TENANT1,
        "tenant2": TENANT2,
        "vendor1": VENDOR1,
        "vendor2": VENDOR2,
        "user1": USER1,
        "user2": USER2,
        "user_seeds": USER_SEEDS
    }



@pytest.fixture
def fake_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return private_key, public_key
# =================
# RSA key
# =========
@pytest.fixture
def fake_customer_details():
    return dtos.CustomerDetailsRequestDTO(
            customer_id="customer id",
            name="name here",
            email="email1@gmail.com"
        )

@pytest.fixture
def fake_address():
    return dtos.AddressRequestDTO(
            line1="line 1",
            city="city 1",
            country="country 1",
            line2="line 2 here",
            state="state here",
            postal="postal here"
        )

@pytest.fixture
def fake_jwt_token_handler():
    class JwtTokenHandler:
        def __init__(self, public_key: str, issuer: str, audience: str, algorithm: str):
            self.public_key = public_key
            self.issuer = issuer
            self.audience = audience
            self.algorithm = algorithm

        def decode(self, token: str, secret: Optional[str] = None) -> dict:
            return {
                "sub": USER1,
                "token_type": "Bearer",
                "tenant_id": TENANT1,
                "roles": ["vendor"]
            }
    return JwtTokenHandler





@pytest.fixture
def fake_access_control(fake_jwt_token_handler):

    saas_lookup_service_instance = saas_lookup_service.SaaSLookupService()

    # ============== resolve access control based on tenant_id ===============
    access_control1.AccessControlService.configure(
        saas_lookup_service=saas_lookup_service_instance,
        access_control_library=access_control1.AccessControl1,
        jwt_handler=fake_jwt_token_handler
    )
    return access_control1.AccessControlService

@pytest.fixture(scope="session", autouse=True)
def domain_clock():
    domain_services.DomainClock.configure(clocks.UTCClock())
    return domain_services.DomainClock


# =======================
# JWT fixtures
# ==========

@pytest.fixture()
def fake_exception_handler():
    return exception_handler.OrderExceptionHandler()

@pytest.fixture()
def fake_user_action_service():
    return user_action_service.UserActionService()

@pytest.fixture()
def fake_uow():
    return repositories.DjangoOrderUnitOfWork()

@pytest.fixture()
def fake_jwt_valid_token(fake_rsa_keys):
    private_key, _ = fake_rsa_keys

    payload = {
        "sub": USER1,
        "aud": "my-app",
        "iss":"https://issuer.test",
        "tenant_id": TENANT1,
        "token_type": "Bearer",
        "roles": ["vendor"],
        "exp": datetime.now() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

@pytest.fixture()
def fake_jwt_expired_token(fake_rsa_keys):
    private_key, _ = fake_rsa_keys

    payload = {
        "sub": USER1,
        "aud": "my-app",
        "iss":"https://issuer.test",
        "tenant_id": TENANT1,
        "token_type": "Bearer",
        "roles": ["customer"],
        "exp": datetime.now() - timedelta(minutes=5)
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

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



# =======================
# JWT fixtures
# ==========

# =================
# Seeded Fixtures
# ==============
@pytest.fixture(scope="session", autouse=True)
def seeded_all():
    """
    Equivalent seeder for DynamoDB using Single Table Design.
    """
    # Use environment variables for LocalStack flexibility
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    

    # Lets PreWipe the table first
    # Scan for all keys
    scan = table.scan(ProjectionExpression='pk, sk')
    
    # Batch delete to stay fast
    with table.batch_writer() as batch:
        for each in scan.get('Items', []):
            batch.delete_item(Key={'pk': each['pk'], 'sk': each['sk']})
    # Lets PreWipe the table first

    # Batch writer handles buffering and efficiency
    with table.batch_writer() as batch:
        

        # 1. Tenant Configs
        for tc in TENANT_CONFIG_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{tc[0]}", 
                "sk": "CONFIG#TENANT",
                "configs": tc[1], 
                "last_update_dt": tc[2].isoformat() if hasattr(tc[2], 'isoformat') else tc[2]
            })

        # 2. SaaS Configs
        for sas in SAAS_CONFIG_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{sas[0]}", 
                "sk": "CONFIG#SAAS",
                "configs": sas[1], 
                "last_update_dt": sas[2].isoformat() if hasattr(sas[2], 'isoformat') else sas[2]
            })

        # 3. User Authorizations
        for us in USER_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{us[0]}", 
                "sk": f"AUTH#USER#{us[1]}",
                "scope": us[2],
                "is_active": us[3]
            })

        # 4. Orders (The Header)
        for os_data in ORDER_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{os_data[1]}", 
                "sk": f"ORDER#{os_data[0]}",
                "order_id": os_data[0],
                "tenant_id": os_data[1],   
                "version": os_data[2],
                "external_ref": os_data[3],
                "order_status": os_data[4],
                "customer_id": os_data[5],
                "customer_name": os_data[6],
                "customer_email": os_data[7],
                "payment_status": os_data[8],
                "currency": os_data[9],
                "date_created": os_data[10].isoformat(),
                "date_modified": os_data[11].isoformat(),
                "entity_type": "ORDER"
            })

        # 5. Order Lines
        for ol in ORDER_LINE_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{ol[0]}", 
                "sk": f"LINE#{ol[1]}",
                "product_sku": ol[1],  
                "product_name": ol[2],
                "product_price": Decimal(str(ol[3])),
                "product_currency": ol[4],
                "order_quantity": ol[5],
                "vendor_id": ol[6],
                "package_weight_kg": Decimal(str(ol[7])),
                "entity_type": "LINE_ITEM"
            })

        # 6. Shipments
        for sh in SHIPMENT_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{sh[1]}", 
                "sk": f"SHIPMENT#{sh[0]}",
                "line1": sh[2],
                "line2": sh[3],
                "city": sh[4],
                "postal": sh[5],
                "country": sh[6],
                "state": sh[7],
                "provider": sh[8],
                "tracking": sh[9],
                "amount": Decimal(str(sh[10])),
                "currency": sh[11],
                "status": sh[12],
                "entity_type": "SHIPMENT"
            })


        # 7. Shipment Items (Flattened in DynamoDB)
        for shi in SHIPMENT_ITEM_SEEDS:
            batch.put_item(Item={
                # PK is still the Order ID so we can fetch everything at once
                "pk": f"ORDER#{shi[1]}", # Assuming index 4 is OrderID, or look it up from Shipment
                # Hierarchical SK to group items under their specific shipment
                "sk": f"SHIPMENT#{shi[2]}#ITEM#{shi[0]}#SKU#{shi[3]}",
                "shipment_id": shi[2],
                "shipment_item_id": shi[0],
                "line_item_sku": shi[3], 
                "quantity": shi[4],
                "entity_type": "SHIPMENT_ITEM"
            })


        # 8. User Action Logs
        for ual in USER_ACTION_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{ual[0]}", 
                "sk": f"LOG#{ual[4].isoformat()}#{ual[1]}",
                "action": ual[1],
                "performed_by": ual[2],
                "user_input": ual[3]
            })
    print("✅ DynamoDB Seeding Complete.")

