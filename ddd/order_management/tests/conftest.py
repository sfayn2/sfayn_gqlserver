import pytest, json, jwt
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from decimal import Decimal
from order_management import models as django_snapshots
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

# Columns order_id, tenant_id, external_ref, order_status, customer_id, customer_name, customer_email, payment_status, currency, date_created, date_modified
ORDER_SEEDS = (
    ("ORD-CONFIRMED-1", TENANT1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)), ("ORD-NOTCONFIRMED-1", TENANT1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-DRAFT-1", TENANT1, "external ref here", enums.OrderStatus.DRAFT.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_SHIPPED-1", TENANT1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_PENDING-1", TENANT1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_CONFIRMED-1", TENANT1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_DELIVERED-1", TENANT1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-1", TENANT1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-ALREADY-COMPLETED-1", TENANT1, "external ref here", enums.OrderStatus.COMPLETED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-UNPAID-1", TENANT1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
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
)

# Shipment
# Columns shipment_id, order_id, shipment_address_line1, shipment_address_line2, shipment_address_city, shipment_address_postal, shipment_address_country, shipment_address_state, shipment_provider, tracking_reference, shipment_amount, shipment_currency, shipment_status
SHIPMENT_SEEDS = (
    ("SH-1", "ORD-CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value),
    ("SH-SHIPPED-2", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.SHIPPED.value),
    ("SH-PENDING-2", "ORD-CONFIRMED_W_PENDING-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value),
    ("SH-CONFIRMED-2", "ORD-CONFIRMED_W_CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.CONFIRMED.value),
    ("SH-DELIVERED-2", "ORD-CONFIRMED_W_DELIVERED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-READY-TO-COMPLETE-1", "ORD-READY-TO-COMPLETE-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-ALREADY-COMPLETED-1", "ORD-ALREADY-COMPLETED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
    ("SH-READY-TO-COMPLETE-UNPAID-1", "ORD-READY-TO-COMPLETE-UNPAID-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value),
)


# Shipment Item
# Columns shipment_item_id, shipment_id, line_item_id, quantity
SHIPMENT_ITEM_SEEDS = (
    ("SHI-1", "SH-1", "SKU-A", 1, None, None),
    ("SHI-SHIPPED-1", "SH-SHIPPED-2", "SKU-C", 1),
    ("SHI-PENDING-1", "SH-PENDING-2", "SKU-D", 1),
    ("SHI-CONFIRMED-1", "SH-CONFIRMED-2", "SKU-E", 1),
    ("SHI-DELIVERED-1", "SH-DELIVERED-2", "SKU-F", 1),
    ("SHI-READY-TO-COMPLETE-1", "SH-READY-TO-COMPLETE-1", "SKU-G", 1),
    ("SHI-ALREADY-COMPLETED-1", "SH-ALREADY-COMPLETED-1", "SKU-H", 1),
    ("SHI-READY-TO-COMPLETE-UNPAID-1", "SH-READY-TO-COMPLETE-UNPAID-1", "SKU-I", 1),
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
    ("SaaSOwner", json.dumps({
        "idp": {},
        "webhooks": {
            "shipment_tracker": {
                "provider": "easypost",
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
            "provider": "easypost",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
    (TENANT1, json.dumps({
        "idp": {
            "public_key": "92alSyFzFiPHT3oYDwjXAGXFAAAQGt1Eoaag5dw",
            "issuer": "http://idp.saasprovider.com/realms/saas_owner",
            "audience": "AUD1",
            "algorithm": "RS256",
        },
        "webhooks": {
            "shipment_tracker": {
                "provider": "easypost",
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
            "provider": "easypost",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
)

# === Test Data ========

@pytest.fixture(scope="session", autouse=True)
def test_constants():
    return {
        "tenant1": TENANT1,
        "tenant2": TENANT2,
        "vendor1": VENDOR1,
        "vendor2": VENDOR2,
        "user1": USER1,
        "user2": USER2
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
    return dtos.CustomerDetailsDTO(
            customer_id="customer id",
            name="name here",
            email="email1@gmail.com"
        )

@pytest.fixture
def fake_address():
    return dtos.AddressDTO(
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



# =======================
# JWT fixtures
# ==========

# =================
# Seeded Fixtures
# ==============
@pytest.fixture(scope="session", autouse=True)
def seeded_all(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
# Columns vendor_id, tenant_id, offer_id, coupon_code, start_date, end_date, is_active

        for tc in TENANT_CONFIG_SEEDS:
            django_snapshots.TenantConfig.objects.create(
                tenant_id=tc[0],
                configs=tc[1],
                last_update_dt=tc[2]
            )

        for sas in SAAS_CONFIG_SEEDS:
            django_snapshots.SaaSConfig.objects.create(
                tenant_id=sas[0],
                configs=sas[1],
                last_update_dt=sas[2]
            )


        for us in USER_SEEDS:
            django_snapshots.UserAuthorizationSnapshot.objects.create(
                tenant_id=us[0], 
                permission_codename=us[1],
                scope=us[2],
                is_active=us[3]
            )

        for os in ORDER_SEEDS:
            django_snapshots.Order.objects.create(
                order_id=os[0], 
                tenant_id=os[1], 
                external_ref=os[2], 
                order_status=os[3], 
                customer_id=os[4], 
                customer_name=os[5], 
                customer_email=os[6],
                payment_status=os[7], 
                currency=os[8], 
                date_created=os[9],
                date_modified=os[10]
            )

        for ol in ORDER_LINE_SEEDS:
            django_snapshots.LineItem.objects.create(
                order_id=ol[0], 
                product_sku=ol[1], 
                product_name=ol[2], 
                product_price=ol[3], 
                product_currency=ol[4], 
                order_quantity=ol[5], 
                vendor_id=ol[6], 
                package_weight_kg=ol[7]
            )


        for sh in SHIPMENT_SEEDS:
            django_snapshots.Shipment.objects.create(
                shipment_id=sh[0], 
                order_id=sh[1], 
                shipment_address_line1=sh[2], 
                shipment_address_line2=sh[3], 
                shipment_address_city=sh[4], 
                shipment_address_postal=sh[5], 
                shipment_address_country=sh[6], 
                shipment_address_state=sh[7], 
                shipment_provider=sh[8], 
                tracking_reference=sh[9], 
                shipment_amount=sh[10], 
                shipment_currency=sh[11], 
                shipment_status=sh[12]
            )

        for shi in SHIPMENT_ITEM_SEEDS:
            django_snapshots.ShipmentItem.objects.create(
                shipment_item_id=shi[0], 
                shipment_id=shi[1], 
                line_item_id=shi[2], 
                quantity=shi[3], 
            )

        for ual in USER_ACTION_SEEDS:
            django_snapshots.UserActionLog.objects.create(
                order_id=ual[0], 
                action=ual[1], 
                performed_by=ual[2], 
                user_input=ual[3], 
                executed_at=ual[4]
            )




# =================
# Seeded Fixtures
# ==============