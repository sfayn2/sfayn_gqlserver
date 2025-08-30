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
def fake_product_skus():
    return [
            dtos.ProductSkusDTO(
                vendor_id="vendor-1",
                product_sku="sku1",
                order_quantity=22
            )
        ]

@pytest.fixture
def fake_access_control():
    class FakeAccessControl:

        def ensure_user_is_authorized_for(
            self, token: str, required_permission: str, required_scope: dict = None
        ) -> dtos.Identity:
            return dtos.Identity(
                sub="user-1",
                token_type="Bearer",
                tenant_id="tenant_123",
                roles=["customer"]
            )
    return FakeAccessControl

@pytest.fixture
def fake_vendor_repo():
    class FakeVendorRepo:
        def get_line_items(
            self, 
            tenant_id: str,
            product_skus_input: List[dtos.ProductSkusDTO]
        ) -> List[models.LineItem]:

            return [
                models.LineItem(
                    product_sku="sku1",
                    product_name="my product",
                    product_price=value_objects.Money(
                        amount=Decimal("20"),
                        currency="SGD"
                    ),
                    order_quantity= 10,
                    vendor=value_objects.VendorDetails(
                        vendor_id="vendor-1",
                        name="Just a another vendor",
                        country="Singapore"
                    ),
                    product_category="T-SHIRT",
                    options={
                        "Color": "RED", "Size": "M"
                    },
                    package=value_objects.Package(
                        weight=Decimal("1"),
                        dimensions=(1, 1, 1)
                    ),
                    is_free_gift=False,
                    is_taxable=False
                )
            ]
    return FakeVendorRepo


@pytest.fixture
def fake_vendor_repo_w_free_gift_taxable(fake_vendor_repo):
    class FakeVendorRepo:
        def get_line_items(
            self, 
            tenant_id: str,
            vendor_id: str, 
            product_skus_input: List[dtos.ProductSkusDTO]
        ) -> List[models.LineItem]:

            return [
                models.LineItem(
                    product_sku="sku1",
                    product_name="my product",
                    product_price=value_objects.Money(
                        amount=Decimal("20"),
                        currency="SGD"
                    ),
                    order_quantity= 10,
                    vendor=value_objects.VendorDetails(
                        vendor_id="vendor-1",
                        name="Just a another vendor",
                        country="Singapore"
                    ),
                    product_category="T-SHIRT",
                    options={
                        "Color": "RED", "Size": "M"
                    },
                    package=value_objects.Package(
                        weight=Decimal("1"),
                        dimensions=(1, 1, 1)
                    ),
                    is_free_gift=True,
                    is_taxable=True
                )
            ]
    return FakeVendorRepo

@pytest.fixture
def fake_vendor_repo_w_free_gift_taxable(fake_vendor_repo):
    class FakeVendorRepo:
        def get_line_items(
            self, 
            tenant_id: str,
            product_skus_input: List[dtos.ProductSkusDTO]
        ) -> List[models.LineItem]:

            return [
                models.LineItem(
                    product_sku="sku1",
                    product_name="my product",
                    product_price=value_objects.Money(
                        amount=Decimal("20"),
                        currency="SGD"
                    ),
                    order_quantity= 10,
                    vendor=value_objects.VendorDetails(
                        vendor_id="vendor-1",
                        name="Just a another vendor",
                        country="Singapore"
                    ),
                    product_category="T-SHIRT",
                    options={
                        "Color": "RED", "Size": "M"
                    },
                    package=value_objects.Package(
                        weight=Decimal("1"),
                        dimensions=(1, 1, 1)
                    ),
                    is_free_gift=True,
                    is_taxable=True
                )
            ]
    return FakeVendorRepo


@pytest.fixture
def fake_stock_validation():
    class FakeStockValidation:
        def ensure_items_in_stock(self, tenant_id: str, skus: List[dtos.ProductSkusDTO] ) -> None:
            return None # always ok
    return FakeStockValidation

@pytest.fixture(scope="session", autouse=True)
def domain_clock():
    domain_services.DomainClock.configure(clocks.UTCClock())
    return domain_services.DomainClock

@pytest.fixture
def seeded_vendor_product_snapshot():
    return [
        django_snapshots.VendorProductSnapshot.objects.create(
            product_id="prod-1",
            vendor_id="vendor-1",
            tenant_id="tenant_123",
            product_sku="sku1",
            product_name="my product",
            product_category="T-SHIRT",
            options=json.dumps({"Color": "RED", "Size": "M" }),
            product_price=20,
            stock=0,
            product_currency="SGD",
            package_weight="1",
            package_length="1",
            package_width="1",
            package_height="1",
            is_free_gift=False,
            is_taxable=True,
            is_active=True
        )
    ]

@pytest.fixture
def seeded_vendor_details_snapshot():
    return django_snapshots.VendorDetailsSnapshot.objects.create(
        vendor_id="vendor-1",
        tenant_id="tenant_123",
        name="VendorA",
        country="Singapore",
        is_active=True
    )

# =======================
# JWT fixtures
# ==========

@pytest.fixture()
def fake_jwt_valid_token(fake_rsa_keys):
    private_key, _ = fake_rsa_keys

    payload = {
        "sub": "user-1",
        "aud": "my-app",
        "iss":"https://issuer.test",
        "tenant_id": "tenant_123",
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
        "sub": "user-1",
        "aud": "my-app",
        "iss":"https://issuer.test",
        "tenant_id": "tenant_123",
        "token_type": "Bearer",
        "roles": ["customer"],
        "exp": datetime.now() - timedelta(minutes=5)
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


#@pytest.fixture
#def fake_jwt_token():
#    payload = {
#        "sub": "user-1",
#        "aud": "my-app",
#        "iss":"https://issuer.test",
#        "tenant_id": "tenant_123",
#        "token_type": "Bearer",
#        "roles": ["customer"],
#        "exp": datetime.now() + timedelta(minutes=5)
#    }
#    return jwt.encode(payload, SECRET, algorithm="RS256")

@pytest.fixture
def fake_jwt_handler():
    class FakeJWTHandler:
        def decode(self, token: str) -> dict:
            #jwt_handler = access_control1.JwtTokenHandler(
            #    public_key="fake_public",
            #    algorithm="RS256",
            #    audience="my-app",
            #    issuer="https://issuer.test"
            #)
            #return jwt_handler.decode(
            #    fake_jwt_token(),
            #    SECRET
            #)
            return {
                "sub": "user-1",
                "tenant_id": "tenant_123",
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
    return django_snapshots.UserAuthorizationSnapshot.objects.create(
        user_id="user-1",
        permission_codename="checkout_items",
        tenant_id="tenant_123",
        scope=json.dumps({ "customer_id": "user-1" }),
        is_active=True
    )

@pytest.fixture
def seeded_order():
    return django_snapshots.Order.objects.create(
                order_id="ORD-1",
                order_status=enums.OrderStatus.DRAFT.value,
                cancellation_reason="",
                customer_id="user-1",
                customer_first_name="first name1",
                customer_last_name="last name1",
                customer_email="email@gmail.com",
                coupons=json.dumps([]),
                delivery_street="street1",
                delivery_city="Singapore",
                delivery_postal=1234,
                delivery_country="Singapore",
                delivery_state="Singapore",
                shipping_method=None,
                shipping_delivery_time=None,
                shipping_cost=None,
                shipping_tracking_reference=None,
                tax_details=json.dumps([]),
                tax_amount=Decimal("0"),
                total_discounts_fee=Decimal("0"),
                total_amount=Decimal("0"),
                offer_details=json.dumps([]),
                final_amount=Decimal("0"),
                payment_method=None,
                payment_reference=None,
                payment_amount=Decimal("0"),
                payment_status=None,
                currency="SGD",
                tenant_id="tenant_123"
    )

@pytest.fixture
def seeded_line_items():
    return django_snapshots.OrderLine.objects.create(
        order_id="ORD-1",
        vendor_id="vendor-1",
        vendor_name="Vendor1",
        vendor_country="Singapore",
        product_sku="sku1",
        product_name="my product",
        product_category="T-SHIRT",
        is_free_gift=False,
        is_taxable=True,
        options=json.dumps({"Size": "M", "Color": "RED"}),
        product_price=Decimal("20"),
        product_currency="SGD",
        order_quantity=10,
        package_weight=1,
        package_length=1,
        package_width=1,
        package_height=1,
        total_price=200
    )


# =================
# Seeded Fixtures
# ==============