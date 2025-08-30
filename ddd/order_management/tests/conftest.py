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

USER1 = "user-1"
USER2 = "user-2"
TENANT1 = "tenant_123"
TENANT2 = "tenant_456"
VENDOR1 = "vendor-1"
VENDOR2 = "vendor-2"




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
# TODO should be moving to consumer; this is not global
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
def seeded_all():
    USER_SEEDS = (
        (USER1, "checkout_items", TENANT1, json.dumps({ "customer_id": USER1 }), True),
    )
    for us in USER_SEEDS:
        django_snapshots.UserAuthorizationSnapshot.objects.create(
            user_id=us[0], 
            permission_codename=us[1],
            tenant_id=us[2], 
            scope=us[3],
            is_active=us[4]
        )

    ORDER_SEEDS = (
        ("ORD-1", enums.OrderStatus.DRAFT.value,"", USER1, "first name1", "last name1", "email@gmail.com", json.dumps([]), "street1", "Singapore", 1234, "Singapore", "Singapore", None, None, None, None, json.dumps([]), Decimal("0"), Decimal("0"), Decimal("0"), json.dumps([]), Decimal("0"), None, None, Decimal("0"), None, "SGD", TENANT1),
    )
    for os in ORDER_SEEDS:
        django_snapshots.Order.objects.create(
            order_id=os[0], 
            order_status=os[1],
            cancellation_reason=os[2], 
            customer_id=os[3], 
            customer_first_name=os[4],
            customer_last_name=os[5], 
            customer_email=os[6], 
            coupons=os[7],
            delivery_street=os[8], 
            delivery_city=os[9], 
            delivery_postal=os[10],
            delivery_country=os[11], 
            delivery_state=os[12], 
            shipping_method=os[13],
            shipping_delivery_time=os[14], 
            shipping_cost=os[15], 
            shipping_tracking_reference=os[16],
            tax_details=os[17], 
            tax_amount=os[18], 
            total_discounts_fee=os[19],
            total_amount=os[20], 
            offer_details=os[21], 
            final_amount=os[22],
            payment_method=os[23], 
            payment_reference=os[24], 
            payment_amount=os[25],
            payment_status=os[26], 
            currency=os[27], 
            tenant_id=os[28]
        )

    ORDER_LINE_SEEDS = (
        ("ORD-1", VENDOR1, "Vendor1", "Singapore", "sku1", "my product", "T-SHIRT", False, True, json.dumps({"Size": "M", "Color": "RED"}), Decimal("20"), "SGD", 10, 1, 1, 1, 1, 200),
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

    VENDOR_PRODUCT_SEEDS = (
        ("prod-1", VENDOR1, TENANT1, "sku1_ok", "sample product for checkout items", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
        ("prod-1", VENDOR1, TENANT1, "sku1_out_of_stock", "sample product for checkout items", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", False, True, True),
        ("prod-2", VENDOR1, TENANT1, "sku_w_free_gift", "sample product for checkout items", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "SGD", "1", "1", "1", "1", True, True, True),
        ("prod-3", VENDOR1, TENANT1, "sku_currency_mismatch", "sample product for add line items", "T-SHIRT", json.dumps({"Color": "RED", "Size": "M" }), 20, 999, "USD", "1", "1", "1", "1", False, True, True)
    )

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

    VENDOR_SEEDS = (
        (VENDOR1, TENANT1, "VendorA", "Singapore", True),
    )
    for vs in VENDOR_SEEDS:
        django_snapshots.VendorDetailsSnapshot.objects.create(
            vendor_id=vs[0], 
            tenant_id=vs[1], 
            name=vs[2], 
            country=vs[3], 
            is_active=vs[4]
        )





# =================
# Seeded Fixtures
# ==============