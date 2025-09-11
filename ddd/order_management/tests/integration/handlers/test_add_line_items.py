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
        "valid": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku1_ok", order_quantity=22)],
        "already_exists": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_already_exists", order_quantity=10)],
        "currency_mismatch": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_currency_mismatch", order_quantity=22)],
        "not_draft":  [dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_already_exists", order_quantity=10)],
        "vendor_mismatch": [dtos.ProductSkusDTO(vendor_id=test_constants["vendor2"], product_sku="sku_vendor_mismatch", order_quantity=22)],
    }

@pytest.mark.django_db
@pytest.mark.parametrize(
    "order_id, product_key, expected_success, expected_message",
    [
        ("ORD-1", "valid", True, "successfully add line items."),
        ("ORD-1", "already_exists", False, "Order ORD-1 Line item with SKU sku_already_exists already exists."),
        ("ORD-1", "currency_mismatch", False, "Currency mismatch between order and line item."),
        ("ORD-1", "vendor_mismatch", False, "Vendor mismatch between order and line item."),
        ("ORD-NONDRAFT-1", "not_draft", False, "Only draft order can add line item."),
    ]
)
def test_add_line_items(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    order_id,
    product_key,
    expected_success,
    expected_message
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.AddLineItemsCommand(
        order_id=order_id,
        product_skus=fake_product_skus[product_key]
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_add_line_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        stock_validation=validations.DjangoStockValidation(),
        access_control=fake_access_control(),
        user_ctx=user_ctx
    )


    assert response.success is expected_success
    assert expected_message in response.message
