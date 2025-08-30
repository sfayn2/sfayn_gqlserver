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
    access_control1
)


@pytest.mark.django_db
def test_add_line_items_ok(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_vendor_repo, 
    fake_stock_validation, 
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    seeded_user_auth_snapshot,
    seeded_order,
    seeded_line_items
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
        vendor_repo=fake_vendor_repo(),
        access_control=fake_access_control(),
        stock_validation=fake_stock_validation(),
    )


    assert response.success is True
    assert "successfully add line items." in response.message
