import pytest, json, jwt
from datetime import datetime, timedelta
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
    clocks,
    access_control1
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

# Columns user_id, permission_codename, tenant_id, scope, is_active
USER_SEEDS = (
    (USER1, "checkout_items", TENANT1, json.dumps({ "customer_id": USER1 }), True),
)

# Columns order_id, order_stage, activity_status, cancellation_reason, customer_id, customer_first_name, customer_last_name, customer_email, coupons, delivery_street, delivery_city, delivery_postal, delivery_country, delivery_state, shipping_method, shipping_delivery_time, shipping_cost, shipping_tracking_reference, tax_details, tax_amount, total_discounts_fee, total_amount, offer_details, final_amount, payment_method, payment_reference, payment_amount, payment_status, currency, tenant_id
ORDER_SEEDS = (
    ("ORD-1", enums.OrderStage.DRAFT.value, "NoPendingActivities", "", USER1, "first name1", "last name1", "email@gmail.com", json.dumps([]), "street1", "Singapore", 1234, "Singapore", "Singapore", None, None, None, None, json.dumps([]), Decimal("0"), Decimal("0"), Decimal("0"), json.dumps([]), Decimal("0"), None, None, Decimal("0"), None, "SGD", TENANT1),
    ("ORD-NONDRAFT-1", enums.OrderStage.PENDING.value, "NoPendingActivities", "", USER1, "first name1", "last name1", "email@gmail.com", json.dumps([]), "street1", "Singapore", 1234, "Singapore", "Singapore", None, None, None, None, json.dumps([]), Decimal("0"), Decimal("0"), Decimal("0"), json.dumps([]), Decimal("0"), None, None, Decimal("0"), None, "SGD", TENANT1),
    ("ORD-REMOVEITEMS-1", enums.OrderStage.DRAFT.value, "NoPendingActivities", "", USER1, "first name1", "last name1", "email@gmail.com", json.dumps([]), "street1", "Singapore", 1234, "Singapore", "Singapore", None, None, None, None, json.dumps([]), Decimal("0"), Decimal("0"), Decimal("0"), json.dumps([]), Decimal("0"), None, None, Decimal("0"), None, "SGD", TENANT1),
    ("ORD-CHANGEQTY-1", enums.OrderStage.DRAFT.value, "NoPendingActivities", "", USER1, "first name1", "last name1", "email@gmail.com", json.dumps([]), "street1", "Singapore", 1234, "Singapore", "Singapore", None, None, None, None, json.dumps([]), Decimal("0"), Decimal("0"), Decimal("0"), json.dumps([]), Decimal("0"), None, None, Decimal("0"), None, "SGD", TENANT1),
)

# Columns order_id, vendor_id, vendor_name, vendor_country, product_sku, product_name, product_category, is_free_gift, is_taxable, options, product_price, product_currency, order_quantity, package_weight, package_length, package_width, package_height, total_price
ORDER_LINE_SEEDS = (
    ("ORD-1", VENDOR1, "VendorA", "Singapore", "sku_ok", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-1", VENDOR1, "VendorA", "Singapore", "sku_already_exists", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-NONDRAFT-1", VENDOR1, "VendorA", "Singapore", "sku_already_exists", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-REMOVEITEMS-1", VENDOR1, "VendorA", "Singapore", "sku_remove1", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-REMOVEITEMS-1", VENDOR1, "VendorA", "Singapore", "sku_remove2", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-CHANGEQTY-1", VENDOR1, "VendorA", "Singapore", "sku_change1", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
    ("ORD-CHANGEQTY-1", VENDOR1, "VendorA", "Singapore", "sku_change2", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
)

# order_id, order_stage, activity_status, step, sequence, performed_by, user_input, optional_step, outcome
ORDER_ACTIVITIES = (
    ("ORD-WORKFLOW-TENANT1", "PENDING", "PlaceOrder", "place_order", 1, "user-1", "", False, "WAITING"),
    ("ORD-WORKFLOW-TENANT1", "CONFIRMED", "ConfirmOrder", "confirm_order", 2, "user-1", "", False, "WAITING"),
    ("ORD-WORKFLOW-TENANT1", "SHIPPED", "MarkShipped", "mark_as_shipped", 3, "vendor-1", "", False, "WAITING"),
    ("ORD-WORKFLOW-TENANT1", "COMPLETED", "MarkCompleted", "mark_as_completed", 4, "vendor-1", "", False, "WAITING")
)

# Columns product_id, vendor_id, tenant_id, product_sku, product_name, product_category, options, product_price, stock, product_currency, package_weight, package_length, package_width, package_height, is_free_gift, is_taxable, is_active
VENDOR_PRODUCT_SEEDS = (
    ("prod-0", VENDOR1, TENANT1, "sku_ok", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-1", VENDOR1, TENANT1, "sku1_ok", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-2", VENDOR1, TENANT1, "sku1_out_of_stock", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-3", VENDOR1, TENANT1, "sku_w_free_gift", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", True, True, True),
    ("prod-4", VENDOR1, TENANT1, "sku_currency_mismatch", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "USD", "1", "1", "1", "1", False, True, True),
    ("prod-5", VENDOR1, TENANT1, "sku_free_gift_zero_price", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "USD", "1", "1", "1", "1", True, False, True),
    ("prod-6", VENDOR2, TENANT1, "sku_vendor_mismatch", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-7", VENDOR1, TENANT1, "sku_already_exists", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-8", VENDOR1, TENANT1, "sku_remove1", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-9", VENDOR1, TENANT1, "sku_remove2", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-changeqty-1", VENDOR1, TENANT1, "sku_change1", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
    ("prod-changeqty-2", VENDOR1, TENANT1, "sku_change2", "sample product", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
)

# Columns vendor_id, tenant_id, name, country, is_active
VENDOR_SEEDS = (
    (VENDOR1, TENANT1, "VendorA", "Singapore", True),
    (VENDOR2, TENANT1, "VendorB", "Singapore", True),
)
# === Test Data ========

@pytest.fixture(scope="session", autouse=True)
def test_constants():
    return {
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
            last_name="last name1",
            first_name="first name1",
            email="email1@gmail.com"
        )

@pytest.fixture
def fake_address():
    return dtos.AddressDTO(
            street="street1",
            city="Singapore",
            postal=1234,
            country="Singapore",
            state="Singapore"
        )


@pytest.fixture
def fake_access_control():
    class FakeAccessControl:
        def get_user_context(self, token: str) -> dtos.UserContextDTO:
            return dtos.UserContextDTO(
                sub=USER1,
                token_type="Bearer",
                tenant_id=TENANT1,
                roles=["customer"]
            )

        def ensure_user_is_authorized_for(
            self, user_context: dtos.UserContextDTO, required_permission: str, required_scope: Optional[dict] = None
        ) -> dtos.UserContextDTO:
            return user_context
    return FakeAccessControl

@pytest.fixture(scope="session", autouse=True)
def domain_clock():
    domain_services.DomainClock.configure(clocks.UTCClock())
    return domain_services.DomainClock


# =======================
# JWT fixtures
# ==========

@pytest.fixture()
def fake_jwt_valid_token(fake_rsa_keys):
    private_key, _ = fake_rsa_keys

    payload = {
        "sub": USER1,
        "aud": "my-app",
        "iss":"https://issuer.test",
        "tenant_id": TENANT1,
        "token_type": "Bearer",
        "roles": ["customer"],
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
def fake_jwt_handler():
    class FakeJWTHandler:
        def decode(self, token: str) -> dict:
            return {
                "sub": USER1,
                "tenant_id": TENANT1,
                "token_type": "Bearer",
                "roles": ["customer"]
            }
    return FakeJWTHandler

# =======================
# JWT fixtures
# ==========

# =================
# Seeded Fixtures
# ==============
@pytest.fixture(scope="session", autouse=True)
def seeded_all(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for vp in VENDOR_PRODUCT_SEEDS:
            django_snapshots.VendorProductSnapshot.objects.create(
                product_id=vp[0],
                vendor_id=vp[1],
                tenant_id=vp[2],
                product_sku=vp[3],
                product_name=vp[4],
                product_category=vp[5],
                options=vp[6],
                product_price=vp[7],
                stock=vp[8],
                product_currency=vp[9],
                package_weight=vp[10],
                package_length=vp[11],
                package_width=vp[12],
                package_height=vp[13],
                is_free_gift=vp[14],
                is_taxable=vp[15],
                is_active=vp[16]
            )

        for vs in VENDOR_SEEDS:
            django_snapshots.VendorDetailsSnapshot.objects.create(
                vendor_id=vs[0], 
                tenant_id=vs[1], 
                name=vs[2], 
                country=vs[3], 
                is_active=vs[4]
            )

        for us in USER_SEEDS:
            django_snapshots.UserAuthorizationSnapshot.objects.create(
                user_id=us[0], 
                permission_codename=us[1],
                tenant_id=us[2], 
                scope=us[3],
                is_active=us[4]
            )

        for os in ORDER_SEEDS:
            django_snapshots.Order.objects.create(
                order_id=os[0], 
                order_stage=os[1],
                activity_status=os[2],
                cancellation_reason=os[3], 
                customer_id=os[4], 
                customer_first_name=os[5],
                customer_last_name=os[6], 
                customer_email=os[7], 
                coupons=os[8],
                delivery_street=os[9], 
                delivery_city=os[10], 
                delivery_postal=os[11],
                delivery_country=os[12], 
                delivery_state=os[13], 
                shipping_method=os[14],
                shipping_delivery_time=os[15], 
                shipping_cost=os[16], 
                shipping_tracking_reference=os[17],
                tax_details=os[18], 
                tax_amount=os[19], 
                total_discounts_fee=os[20],
                total_amount=os[21], 
                offer_details=os[22], 
                final_amount=os[23],
                payment_method=os[24], 
                payment_reference=os[25], 
                payment_amount=os[26],
                payment_status=os[27], 
                currency=os[28], 
                tenant_id=os[29]
            )

        for ol in ORDER_LINE_SEEDS:
            django_snapshots.OrderLine.objects.create(
                order_id=ol[0],
                vendor_id=ol[1],
                vendor_name=ol[2],
                vendor_country=ol[3],
                product_sku=ol[4],
                product_name=ol[5],
                product_category=ol[6],
                is_free_gift=ol[7],
                is_taxable=ol[8],
                options=ol[9],
                product_price=ol[10],
                product_currency=ol[11],
                order_quantity=ol[12],
                package_weight=ol[13], 
                package_length=ol[14], 
                package_width=ol[15],
                package_height=ol[16], 
                total_price=ol[17]
            )






# =================
# Seeded Fixtures
# ==============