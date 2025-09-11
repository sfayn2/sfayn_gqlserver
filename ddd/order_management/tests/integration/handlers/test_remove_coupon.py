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

@pytest.mark.django_db
@pytest.mark.parametrize(
    "order_id, coupon_code, expected_success, expected_message",
    [
        ("ORD-1", "VALID-COUPON25", True, "Order ORD-1 successfully remove coupon."),
    ]
)
def test_remove_coupon(
    fake_jwt_handler, 
    fake_access_control,
    domain_clock,
    order_id,
    coupon_code,
    expected_success,
    expected_message
):

    access_control = access_control1.AccessControl1(
        jwt_handler=fake_jwt_handler()
    )

    command = commands.RemoveCouponCommand(
        order_id=order_id,
        coupon_code=coupon_code
    )

    user_ctx = fake_access_control().get_user_context(token="fake_jwt_token")

    response = handlers.handle_remove_coupon(
        command=command,
        uow=infra_repo.DjangoOrderUnitOfWork(),
        access_control=fake_access_control(),
        coupon_validation=validations.DjangoCouponValidation(),
        user_ctx=user_ctx
    )


    assert response.success is expected_success
    assert response.message == expected_message
