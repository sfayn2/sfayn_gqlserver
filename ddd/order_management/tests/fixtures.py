import pytest, jwt, os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from typing import Optional
from datetime import datetime, timedelta
from ddd.order_management.application import dtos
from ddd.order_management.domain import (
    models,
    repositories as domain_ports,
    services as domain_services,
    value_objects,
    exceptions,
    enums
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
from .data import (
    TENANT_CONFIG_SEEDS,
    SAAS_CONFIG_SEEDS,
    USER_SEEDS,
    ORDER_SEEDS,
    ORDER_LINE_SEEDS,
    SHIPMENT_SEEDS,
    SHIPMENT_ITEM_SEEDS,
    USER_ACTION_SEEDS,
    SAAS1,
    TENANT1,
    TENANT2,
    VENDOR1,
    VENDOR2,
    USER1,
    USER2,
    JWT_VENDOR_PAYLOAD,
    JWT_EXPIRED_CUSTOMER_PAYLOAD
)        




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
            return JWT_VENDOR_PAYLOAD
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
        "typ": "Bearer",
        "organization": [TENANT1],
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
        "typ": "Bearer",
        "organization": [TENANT1],
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