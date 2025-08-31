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
    validations
)


@pytest.fixture
def fake_product_skus_w_free_gift_zero_price(test_constants):
    return [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_free_gift_zero_price", order_quantity=1)]

@pytest.mark.django_db
def test_checkout_items_freegift_zero_price(
    fake_customer_details,
    fake_address,
    fake_product_skus_w_free_gift_zero_price,
    fake_access_control, 
    domain_clock,
    seeded_all
):

    command = commands.CheckoutItemsCommand(
        token="fake_jwt_token",
        customer_details=fake_customer_details,
        address=fake_address,
        product_skus=fake_product_skus_w_free_gift_zero_price
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
    assert response.message ==  "Free gifts must have a price of zero."
