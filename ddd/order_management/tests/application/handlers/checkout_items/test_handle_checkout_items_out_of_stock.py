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
    validations
)


@pytest.mark.django_db
def test_handle_checkout_items_out_of_stock(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_access_control, 
    domain_clock,
    seeded_vendor_product_snapshot,
    seeded_vendor_details_snapshot
):

    command = commands.CheckoutItemsCommand(
        token="fake_jwt_token",
        customer_details=fake_customer_details,
        address=fake_address,
        product_skus=fake_product_skus
    )

    response = handlers.handle_checkout_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        stock_validation=validations.DjangoStockValidation(),
        access_control=fake_access_control(),
        order_service=domain_services.OrderService()
    )

    assert response.success is False
    assert response.message ==  "Product sku1 has only 0 remaining stock/s."
