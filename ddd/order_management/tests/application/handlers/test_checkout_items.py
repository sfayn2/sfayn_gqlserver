import pytest, os, json, time
from typing import List
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.urls import reverse
from order_management import models as django_snapshots
from ddd.order_management.domain import (
    models,
    repositories as domain_ports,
    services as domain_services,
    value_objects
)
from ddd.order_management.application import (
    dtos, 
    commands,
    handlers,
    ports
)
from ddd.order_management.infrastructure import (
    access_control1,
    repositories as infra_ports,
    clocks
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sfayn_gqlserver.settings')
import django
django.setup()

domain_services.DomainClock.configure(clocks.UTCClock())

class FakeAccessControl:
    def ensure_user_is_authorized_for(
        self, token: str, required_permission: str, required_scope: dict = None
    ) -> dtos.UserLoggedInIntegrationEvent:
        identity = dtos.Identity(
            sub="user-1",
            token_type="Bearer",
            tenant_id="tenant-123",
            roles=["customer"]
        )
        return dtos.UserLoggedInIntegrationEvent(
            event_type="identity_gateway_service.external_events.UserLoggedInEvent",
            data=identity
        )

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
                is_free_gift=False,
                is_taxable=False
            )
        ]


class FakeStockValidation:
    def ensure_items_in_stock(self, tenant_id: str, items: List[models.LineItem]) -> None:
        return None # always ok


@pytest.mark.django_db
def test_handle_checkout_items():

    command = commands.CheckoutItemsCommand(
        token="fake_jwt_token",
        vendor_id="vendor-1",
        customer_details=dtos.CustomerDetailsDTO(
            last_name="last name1",
            first_name="first name1",
            email="email1@gmail.com"
        ),
        address=dtos.AddressDTO(
            street="street1",
            city="city1",
            postal=1234,
            country="Singapore",
            state="Singapore"
        ),
        product_skus=[
            dtos.ProductSkusDTO(
                product_sku="Laptop",
                order_quantity=1
            )
        ]
    )

    response = handlers.handle_checkout_items(
        command=command,
        uow=infra_ports.DjangoOrderUnitOfWork(),
        vendor_repo=FakeVendorRepo(),
        stock_validation=FakeStockValidation(),
        access_control=FakeAccessControl(),
        order_service=domain_services.OrderService()
    )

    assert response.success is True
    assert response.message ==  "Cart items successfully checkout."
