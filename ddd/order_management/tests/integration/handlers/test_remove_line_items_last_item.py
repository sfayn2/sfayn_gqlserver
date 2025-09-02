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
    return [
        dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_remove1", order_quantity=22),
        dtos.ProductSkusDTO(vendor_id=test_constants["vendor1"], product_sku="sku_remove2", order_quantity=22)
    ]

@pytest.mark.django_db
def test_remove_line_items_last_item(
    fake_customer_details,
    fake_address,
    fake_product_skus,
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.RemoveLineItemsCommand(
        order_id="ORD-REMOVEITEMS-1",
        product_skus=fake_product_skus
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_remove_line_items(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        vendor_repo=infra_repo.DjangoVendorRepositoryImpl(),
        access_control=fake_access_control(),
        user_ctx=user_ctx
    )


    assert response.success is False
    assert response.message == "Cannot remove the last item. Please cancel the order instead."
