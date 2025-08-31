import pytest, os, json, time
from ddd.order_management.application import (
    commands,
    handlers,
    dtos
)
from ddd.order_management.domain import (
    services as domain_services,
)
from ddd.order_management.infrastructure import (
    repositories as infra_repo,
    access_control1,
    validations
)

@pytest.fixture
def fake_product_skus_different_currency(test_constants):
    return [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_currency_mismatch", order_quantity=22)]

@pytest.mark.django_db
def test_add_line_items_currency_mismatch(
    fake_customer_details,
    fake_address,
    fake_product_skus_different_currency,
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    seeded_all
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.AddLineItemsCommand(
        token="fake_jwt_token",
        order_id="ORD-1",
        product_skus=fake_product_skus_different_currency
    )

    response = handlers.handle_add_line_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        stock_validation=validations.DjangoStockValidation(),
        access_control=fake_access_control(),
    )


    assert response.success is False
    assert response.message == "Currency mismatch between order and line item."
