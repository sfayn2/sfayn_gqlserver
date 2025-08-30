import pytest, os, json, time
from ddd.order_management.application import (
    commands,
    handlers
)
from ddd.order_management.domain import (
    services as domain_services,
)
from ddd.order_management.infrastructure import (
    repositories as infra_repo,
    access_control1,
    validations
)


@pytest.mark.django_db
def test_add_line_items_ok(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    seeded_order,
    seeded_line_items,
    seeded_user_auth_snapshot,
    seeded_vendor_product_snapshot,
    seeded_vendor_details_snapshot
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.AddLineItemsCommand(
        token="fake_jwt_token",
        order_id="ORD-1",
        product_skus=fake_product_skus
    )

    response = handlers.handle_add_line_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        stock_validation=validations.DjangoStockValidation(),
        access_control=fake_access_control(),
    )


    assert response.success is True
    assert "successfully add line items." in response.message
