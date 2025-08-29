import pytest, json
from typing import List
from decimal import Decimal
from order_management import models as django_snapshots
from ddd.order_management.domain import (
    models,
    repositories as domain_ports,
    services as domain_services,
    value_objects,
    exceptions
)
from ddd.order_management.application import (
    dtos, 
)
from ddd.order_management.infrastructure import (
    clocks
)

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
            city="city1",
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
        ) -> dtos.UserLoggedInIntegrationEvent:
            identity = dtos.Identity(
                sub="user-1",
                token_type="Bearer",
                tenant_id="tenant_123",
                roles=["customer"]
            )
            return dtos.UserLoggedInIntegrationEvent(
                event_type="identity_gateway_service.external_events.UserLoggedInEvent",
                data=identity
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
