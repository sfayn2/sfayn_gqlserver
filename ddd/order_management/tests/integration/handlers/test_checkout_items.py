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
def fake_product_skus(test_constants):
    return { 
        "valid" : [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku1_ok", order_quantity=22)],
        "out_of_stock": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku1_out_of_stock", order_quantity=1000)],
        "free_gift_zero_price": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_free_gift_zero_price", order_quantity=1)],
        "free_gift_not_taxable": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_w_free_gift", order_quantity=22)]
    }

@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_key, expected_success, expected_message",
    [
        ("valid", True, "Cart items successfully checkout."),
        ("out_of_stock", False, "Product sku1_out_of_stock has only 999 remaining stock/s."),
        ("free_gift_zero_price", False, "Free gifts must have a price of zero."),
        ("free_gift_not_taxable", False, "Free gift is not taxable."),
    ]
)
def test_checkout_items(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    product_key,
    expected_success,
    expected_message
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.CheckoutItemsCommand(
        customer_details=fake_customer_details,
        address=fake_address,
        product_skus=fake_product_skus[product_key]
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_checkout_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        stock_validation=validations.DjangoStockValidation(),
        access_control=fake_access_control(),
        order_service=domain_services.OrderService(),
        user_ctx=user_ctx
    )

    assert response.success is expected_success
    assert response.message ==  expected_message
