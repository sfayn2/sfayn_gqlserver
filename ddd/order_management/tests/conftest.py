import pytest, json, jwt
from datetime import datetime, timedelta
from typing import List
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

VENDOR1 = "vendor-1"
TENANT1 = "tenant_123"
USER1 = "user-1"

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

# ===========
# fake products input
# ========
@pytest.fixture
def fake_product_skus():
    return [dtos.ProductSkusDTO(vendor_id=VENDOR1, product_sku="sku1_ok", order_quantity=22)]

@pytest.fixture
def fake_product_skus_out_of_stock():
    return [dtos.ProductSkusDTO(vendor_id=VENDOR1, product_sku="sku1_out_of_stock", order_quantity=1000)]

@pytest.fixture
def fake_product_skus_w_free_gift():
    return [dtos.ProductSkusDTO(vendor_id=VENDOR1, product_sku="sku_w_free_gift", order_quantity=22)]

@pytest.fixture
def fake_product_skus_different_currency():
    return [dtos.ProductSkusDTO(vendor_id=VENDOR1, product_sku="sku_currency_mismatch", order_quantity=22)]
# ===========
# fake products input
# ========


@pytest.fixture
def fake_access_control():
    class FakeAccessControl:

        def ensure_user_is_authorized_for(
            self, token: str, required_permission: str, required_scope: dict = None
        ) -> dtos.Identity:
            return dtos.Identity(
                sub=USER1,
                token_type="Bearer",
                tenant_id=TENANT1,
                roles=["customer"]
            )
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
@pytest.fixture
def seeded_user_auth_snapshot():
    return [
        django_snapshots.UserAuthorizationSnapshot.objects.create(user_id=USER1, permission_codename="checkout_items", 
            tenant_id=TENANT1, scope=json.dumps({ "customer_id": USER1 }), is_active=True)
    ]


@pytest.fixture
def seeded_order():
    return [
        django_snapshots.Order.objects.create(order_id="ORD-1", order_status=enums.OrderStatus.DRAFT.value,
                cancellation_reason="", customer_id=USER1, customer_first_name="first name1",
                customer_last_name="last name1", customer_email="email@gmail.com", coupons=json.dumps([]),
                delivery_street="street1", delivery_city="Singapore", delivery_postal=1234,
                delivery_country="Singapore", delivery_state="Singapore", shipping_method=None,
                shipping_delivery_time=None, shipping_cost=None, shipping_tracking_reference=None,
                tax_details=json.dumps([]), tax_amount=Decimal("0"), total_discounts_fee=Decimal("0"),
                total_amount=Decimal("0"), offer_details=json.dumps([]), final_amount=Decimal("0"),
                payment_method=None, payment_reference=None, payment_amount=Decimal("0"),
                payment_status=None, currency="SGD", tenant_id=TENANT1
        )
    ]

@pytest.fixture
def seeded_line_items():
    return [
        django_snapshots.OrderLine.objects.create(
        order_id="ORD-1", vendor_id=VENDOR1, vendor_name="Vendor1", vendor_country="Singapore",
        product_sku="sku1", product_name="my product", product_category="T-SHIRT", is_free_gift=False,
        is_taxable=True, options=json.dumps({"Size": "M", "Color": "RED"}), product_price=Decimal("20"),
        product_currency="SGD", order_quantity=10, package_weight=1, package_length=1, package_width=1,
        package_height=1, total_price=200)
    ]

@pytest.fixture
def seeded_vendor_product_snapshot():
    return [
        django_snapshots.VendorProductSnapshot.objects.create(product_id="prod-1",vendor_id=VENDOR1,
            tenant_id=TENANT1, product_sku="sku1_ok", product_name="sample product for checkout items", product_category="T-SHIRT",
            options=json.dumps({"Color": "RED", "Size": "M" }), product_price=20, stock=999, product_currency="SGD",
            package_weight="1", package_length="1", package_width="1", package_height="1",is_free_gift=False,
            is_taxable=True, is_active=True),
        django_snapshots.VendorProductSnapshot.objects.create(product_id="prod-1",vendor_id=VENDOR1,
            tenant_id=TENANT1, product_sku="sku1_out_of_stock", product_name="sample product for checkout items", product_category="T-SHIRT",
            options=json.dumps({"Color": "RED", "Size": "M" }), product_price=20, stock=999, product_currency="SGD",
            package_weight="1", package_length="1", package_width="1", package_height="1",is_free_gift=False,
            is_taxable=True, is_active=True),
        django_snapshots.VendorProductSnapshot.objects.create(product_id="prod-2",vendor_id=VENDOR1,
            tenant_id=TENANT1, product_sku="sku_w_free_gift", product_name="sample product for checkout items", product_category="T-SHIRT",
            options=json.dumps({"Color": "RED", "Size": "M" }), product_price=20, stock=999, product_currency="SGD",
            package_weight="1", package_length="1", package_width="1", package_height="1", is_free_gift=True,
            is_taxable=True, is_active=True),
        django_snapshots.VendorProductSnapshot.objects.create(product_id="prod-3",vendor_id=VENDOR1,
            tenant_id=TENANT1, product_sku="sku_currency_mismatch", product_name="sample product for add line items", product_category="T-SHIRT",
            options=json.dumps({"Color": "RED", "Size": "M" }), product_price=20, stock=999, product_currency="USD",
            package_weight="1", package_length="1", package_width="1", package_height="1", is_free_gift=False,
            is_taxable=True, is_active=True)
    ]

@pytest.fixture
def seeded_vendor_details_snapshot():
    return [
        django_snapshots.VendorDetailsSnapshot.objects.create(
            vendor_id=VENDOR1, tenant_id=TENANT1, name="VendorA", country="Singapore", is_active=True
        )
    ]



# =================
# Seeded Fixtures
# ==============